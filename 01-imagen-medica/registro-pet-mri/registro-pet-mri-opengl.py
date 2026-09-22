"""
Tarea 9. Alineacion de imagenes medicas multimodales (PET-MRI) de cabeza humana.
Variante con OpenGL: el paso "A Transformar" del diagrama de flujo del PDF
(diapositiva "Alineacion rigida") se ejecuta en GPU mediante un shader, en vez
de usar el resampler de SimpleITK.

Pipeline (mismo diagrama de la diapositiva 5):
    T inicial --> A Transformar (shader OpenGL) --> Medida de Similitud (IMN, numpy)
        --> T es la optima? (scipy.optimize) --> Actualizando T --> ... --> T Final

Imagen Referencia (fija) : MRI.png
Imagen Objetivo  (movil) : PET.png
Medida de similitud      : Informacion Mutua Normalizada (IMN), igual formula
                            que en la diapositiva "Informacion Mutua Normalizada".
Metodo de optimizacion   : Powell (sin derivadas; la metrica viene de un
                            histograma 2D, no es diferenciable de forma analitica
                            al leerse desde la GPU).

Librerias necesarias (todas via pip):
    pip install PyOpenGL PyOpenGL_accelerate glfw numpy scipy matplotlib pillow
"""

import os
import ctypes

import numpy as np
from PIL import Image
import glfw
from OpenGL.GL import *
from scipy.optimize import minimize
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PET_PATH = os.path.join(BASE_DIR, "PET.png")
MRI_PATH = os.path.join(BASE_DIR, "MRI.png")
OUT_PATH = os.path.join(BASE_DIR, "resultado_alineacion_opengl.png")
TAM = 256

VERTEX_SRC = """
#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aTex;
out vec2 vTex;
uniform float uAngulo;        // rotacion rigida, radianes
uniform vec2  uTraslacionNDC; // traslacion en coordenadas normalizadas [-1,1]
void main() {
    float c = cos(uAngulo);
    float s = sin(uAngulo);
    mat2 R = mat2(c, s, -s, c);
    vec2 p = R * aPos + uTraslacionNDC;
    gl_Position = vec4(p, 0.0, 1.0);
    vTex = aTex;
}
"""

FRAGMENT_SRC = """
#version 330 core
in vec2 vTex;
out vec4 FragColor;
uniform sampler2D uTex;
void main() {
    float v = texture(uTex, vTex).r;
    FragColor = vec4(v, v, v, 1.0);
}
"""


# ---------------------------------------------------------------------------
# Utilidades de imagen
# ---------------------------------------------------------------------------

def cargar_como_array_float(path):
    img = Image.open(path).convert("L")
    arr = np.asarray(img, dtype=np.float32)
    arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    return arr


def centro_de_masa(arr):
    h, w = arr.shape
    ys, xs = np.indices((h, w))
    total = arr.sum() + 1e-8
    cx = (xs * arr).sum() / total
    cy = (ys * arr).sum() / total
    return cx, cy


def informacion_mutua_normalizada(a, b, bins=32, umbral=0.05):
    """IMN tal como en la diapositiva 'Informacion Mutua Normalizada':
    I(fR,fT) = (sum_px p log p + sum_py p log p) / (sum_pxy p log p) = (Hx+Hy)/Hxy

    Se excluyen del histograma los pixeles de fondo (negro en ambas imagenes):
    si no se hace esto, el optimizador puede "ganar" IMN simplemente rotando
    la imagen movil fuera del area util, ya que el fondo coincidiria de forma
    trivial en ambas imagenes (minimo espurio).
    """
    mascara = (a > umbral) | (b > umbral)
    if mascara.sum() < 50:
        return 0.0
    a, b = a[mascara], b[mascara]

    a_q = np.clip((a * (bins - 1)).astype(np.int32), 0, bins - 1)
    b_q = np.clip((b * (bins - 1)).astype(np.int32), 0, bins - 1)
    hist2d, _, _ = np.histogram2d(
        a_q.ravel(), b_q.ravel(), bins=bins, range=[[0, bins], [0, bins]]
    )
    pxy = hist2d / hist2d.sum()
    px = pxy.sum(axis=1)
    py = pxy.sum(axis=0)

    nz = pxy > 0
    hxy = -np.sum(pxy[nz] * np.log(pxy[nz]))
    hx = -np.sum(px[px > 0] * np.log(px[px > 0]))
    hy = -np.sum(py[py > 0] * np.log(py[py > 0]))
    return (hx + hy) / hxy if hxy > 0 else 0.0


# ---------------------------------------------------------------------------
# Capa OpenGL: contexto, shaders, FBO y la funcion de "transformar"
# ---------------------------------------------------------------------------

class TransformadorGPU:
    """Encapsula el contexto OpenGL y aplica T(angulo,dx,dy) a la imagen movil,
    devolviendo el resultado remuestreado sobre la malla de la imagen fija
    (equivalente a sitk.Resample, pero ejecutado en GPU)."""

    def __init__(self, tam):
        self.tam = tam
        if not glfw.init():
            raise RuntimeError("No se pudo inicializar GLFW")

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        self.ventana = glfw.create_window(tam, tam, "offscreen-registro", None, None)
        if not self.ventana:
            glfw.terminate()
            raise RuntimeError("No se pudo crear el contexto OpenGL (ventana oculta)")
        glfw.make_context_current(self.ventana)

        print("Contexto OpenGL creado:")
        print("  GL_VERSION  :", glGetString(GL_VERSION).decode())
        print("  GL_RENDERER :", glGetString(GL_RENDERER).decode())

        self.programa = self._crear_programa()
        self.loc_angulo = glGetUniformLocation(self.programa, "uAngulo")
        self.loc_traslacion = glGetUniformLocation(self.programa, "uTraslacionNDC")
        self.loc_tex = glGetUniformLocation(self.programa, "uTex")

        self._crear_quad()
        self.tex_movil = None
        self.fbo, self.tex_destino = self._crear_fbo(tam)

    @staticmethod
    def _compilar_shader(src, tipo):
        sh = glCreateShader(tipo)
        glShaderSource(sh, src)
        glCompileShader(sh)
        if not glGetShaderiv(sh, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(sh).decode())
        return sh

    def _crear_programa(self):
        vs = self._compilar_shader(VERTEX_SRC, GL_VERTEX_SHADER)
        fs = self._compilar_shader(FRAGMENT_SRC, GL_FRAGMENT_SHADER)
        prog = glCreateProgram()
        glAttachShader(prog, vs)
        glAttachShader(prog, fs)
        glLinkProgram(prog)
        if not glGetProgramiv(prog, GL_LINK_STATUS):
            raise RuntimeError(glGetProgramInfoLog(prog).decode())
        glDeleteShader(vs)
        glDeleteShader(fs)
        return prog

    def _crear_quad(self):
        # pos.x, pos.y, tex.u, tex.v  (tex.v invertido: fila 0 del arreglo = arriba)
        quad = np.array([
            -1.0, -1.0, 0.0, 1.0,
             1.0, -1.0, 1.0, 1.0,
             1.0,  1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 0.0,
        ], dtype=np.float32)
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, quad.nbytes, quad, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        stride = 4 * 4
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

    @staticmethod
    def _crear_fbo(tam):
        tex_destino = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_destino)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, tam, tam, 0, GL_RED, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex_destino, 0)
        estado = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if estado != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError(f"FBO incompleto: {estado}")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return fbo, tex_destino

    def subir_imagen_movil(self, arr):
        self.tex_movil = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex_movil)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, arr.shape[1], arr.shape[0],
                     0, GL_RED, GL_FLOAT, arr.astype(np.float32))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    def transformar(self, angulo, tx_ndc, ty_ndc):
        """Aplica T(angulo,dx,dy) a la imagen movil y regresa el resultado
        remuestreado (tam x tam, float32 en [0,1]), ya en convencion
        'fila 0 = arriba' para que coincida con los arreglos numpy."""
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.tam, self.tam)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.programa)
        glUniform1f(self.loc_angulo, float(angulo))
        glUniform2f(self.loc_traslacion, float(tx_ndc), float(ty_ndc))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_movil)
        glUniform1i(self.loc_tex, 0)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        datos = glReadPixels(0, 0, self.tam, self.tam, GL_RED, GL_FLOAT)
        arr = np.frombuffer(datos, dtype=np.float32).reshape(self.tam, self.tam).copy()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return np.flipud(arr)

    def cerrar(self):
        glfw.destroy_window(self.ventana)
        glfw.terminate()


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    fr_arr = cargar_como_array_float(MRI_PATH)   # Imagen Referencia
    ft_arr = cargar_como_array_float(PET_PATH)    # Imagen Objetivo

    gpu = TransformadorGPU(TAM)
    gpu.subir_imagen_movil(ft_arr)

    # --- T inicial: alineacion de centros de masa (equivalente a MOMENTS) -----
    cx_r, cy_r = centro_de_masa(fr_arr)
    cx_t, cy_t = centro_de_masa(ft_arr)
    tx0 = 2.0 * (cx_r - cx_t) / TAM
    ty0 = -2.0 * (cy_r - cy_t) / TAM  # eje y de NDC apunta al reves que las filas
    params0 = np.array([0.0, tx0, ty0])

    historial = []

    def costo(params):
        angulo, tx, ty = params
        warp = gpu.transformar(angulo, tx, ty)
        imn = informacion_mutua_normalizada(fr_arr, warp)
        historial.append(imn)
        return -imn  # se maximiza la IMN -> se minimiza su negativo

    # Rango de busqueda acotado (captura razonable para un registro rigido):
    # +-20 grados de rotacion, +-0.5 en NDC (= +-64 px) de traslacion.
    cotas = [(-0.35, 0.35), (-0.5, 0.5), (-0.5, 0.5)]

    print("\nIniciando registro rigido PET -> MRI (IMN + Powell, transform. en GPU)")
    resultado = minimize(
        costo, params0, method="Powell", bounds=cotas,
        options={"maxiter": 200, "xtol": 1e-3, "ftol": 1e-5, "disp": True},
    )

    angulo_f, tx_f, ty_f = resultado.x

    # --- Imagenes inicial y final, vistas con la GPU ---------------------------
    objetivo_inicial_arr = gpu.transformar(*params0)
    objetivo_alineado_arr = gpu.transformar(angulo_f, tx_f, ty_f)
    gpu.cerrar()

    dif_antes = np.abs(fr_arr - objetivo_inicial_arr)
    dif_despues = np.abs(fr_arr - objetivo_alineado_arr)
    print(f"\n  |dif| promedio antes del registro    : {dif_antes.mean():.4f}")
    print(f"  |dif| promedio despues del registro  : {dif_despues.mean():.4f}")

    # --- Graficas ----------------------------------------------------------------
    fig, ejes = plt.subplots(2, 3, figsize=(13, 9))

    ejes[0, 0].imshow(fr_arr, cmap="gray")
    ejes[0, 0].set_title("Imagen Referencia (MRI)")

    ejes[0, 1].imshow(ft_arr, cmap="hot")
    ejes[0, 1].set_title("Imagen Objetivo (PET) original")

    ejes[0, 2].imshow(objetivo_alineado_arr, cmap="hot")
    ejes[0, 2].set_title("PET alineado (resultado)")

    ejes[1, 0].imshow(dif_antes, cmap="gray")
    ejes[1, 0].set_title("Diferencia ANTES")

    ejes[1, 1].imshow(dif_despues, cmap="gray")
    ejes[1, 1].set_title("Diferencia DESPUES (final)")

    ejes[1, 2].axis("off")

    for ax in (ejes[0, 0], ejes[0, 1], ejes[0, 2], ejes[1, 0], ejes[1, 1]):
        ax.axis("off")

    fig.suptitle(
        "Alineacion rigida PET-MRI",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=150)
    print(f"\nFigura guardada en: {OUT_PATH}")
    plt.show()


if __name__ == "__main__":
    main()
