"""
Se experimenta variando
    a) el tipo de wavelet      : Haar, Daubechies, Symlets, Biorthogonal
    b) el numero de escalas    : 1 a 5 niveles
    c) la regla de seleccion de coeficientes de detalle
"""

import os
import ctypes

import numpy as np
import cv2
import pywt
import matplotlib.pyplot as plt
import glfw
from OpenGL.GL import *
from scipy.optimize import minimize

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MRI_PATH = os.path.join(BASE_DIR, "MRI.png")
PET_PATH = os.path.join(BASE_DIR, "PET.png")

MAX_ABS, PROMEDIO, PRIORIDAD_MRI, PRIORIDAD_PET = 0, 1, 2, 3
NOMBRE_REGLA = {
    MAX_ABS: "Máximo absoluto",
    PROMEDIO: "Promedio",
    PRIORIDAD_MRI: "MRI prio",
    PRIORIDAD_PET: "PET Prio",
}

VERTEX_SRC = """
#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aTex;
out vec2 vTex;
uniform float uAngulo;
uniform vec2  uTraslacionNDC;
void main() {
    float c = cos(uAngulo);
    float s = sin(uAngulo);
    mat2 R = mat2(c, s, -s, c);
    vec2 p = R * aPos + uTraslacionNDC;
    gl_Position = vec4(p, 0.0, 1.0);
    vTex = aTex;
}
"""

# Fragment shader del paso A (Tarea 9): remuestrea una sola textura movil.
FRAGMENT_SRC_TRANSFORMAR = """
#version 330 core
in vec2 vTex;
out vec4 FragColor;
uniform sampler2D uTex;
void main() {
    float v = texture(uTex, vTex).r;
    FragColor = vec4(v, v, v, 1.0);
}
"""

# Fragment shader del paso B (Tarea 10): aplica, pixel a pixel, la regla de
# fusion entre los coeficientes wavelet de MRI (uA) y de PET (uB).
FRAGMENT_SRC_FUSIONAR = """
#version 330 core
in vec2 vTex;
out vec4 FragColor;
uniform sampler2D uA;
uniform sampler2D uB;
uniform int uModo;   // 0=max_abs 1=promedio 2=prioridad_mri 3=prioridad_pet
uniform float uWA;
uniform float uWB;
void main() {
    float a = texture(uA, vTex).r;
    float b = texture(uB, vTex).r;
    float r;
    if (uModo == 0)      r = (abs(a) >= abs(b)) ? a : b;
    else if (uModo == 1) r = uWA * a + uWB * b;
    else if (uModo == 2) r = a;
    else                 r = b;
    FragColor = vec4(r, r, r, 1.0);
}
"""


# ---------------------------------------------------------------------------
# Utilidades de imagen
# ---------------------------------------------------------------------------

def cargar_gris(path):
    """Lee un PNG (color o gris) y lo regresa como arreglo 2D float32 en [0, 1].
    El PET se guarda con el colormap 'hot'; al convertir a gris se obtiene su
    luminancia, que crece de forma monotona con la actividad metabolica real."""
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    arr = img.astype(np.float32)
    arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    return arr


def centro_de_masa(arr):
    h, w = arr.shape
    ys, xs = np.indices((h, w))
    total = arr.sum() + 1e-8
    cx = (xs * arr).sum() / total
    cy = (ys * arr).sum() / total
    return cx, cy


def imn_alineacion(a, b, bins=32, umbral=0.05):
    """Informacion Mutua Normalizada usada como medida de similitud para el
    registro (igual formula que en "Tarea 9.py"): I(fR,fT) = (Hx+Hy)/Hxy.
    Se excluye el fondo (negro en ambas imagenes) para evitar el minimo
    espurio en el que el optimizador "gana" IMN sacando la imagen movil
    fuera del area util."""
    mascara = (a > umbral) | (b > umbral)
    if mascara.sum() < 50:
        return 0.0
    a, b = a[mascara], b[mascara]
    a_q = np.clip((a * (bins - 1)).astype(np.int32), 0, bins - 1)
    b_q = np.clip((b * (bins - 1)).astype(np.int32), 0, bins - 1)
    hist2d, _, _ = np.histogram2d(a_q.ravel(), b_q.ravel(), bins=bins,
                                   range=[[0, bins], [0, bins]])
    pxy = hist2d / hist2d.sum()
    px, py = pxy.sum(axis=1), pxy.sum(axis=0)
    nz = pxy > 0
    hxy = -np.sum(pxy[nz] * np.log(pxy[nz]))
    hx = -np.sum(px[px > 0] * np.log(px[px > 0]))
    hy = -np.sum(py[py > 0] * np.log(py[py > 0]))
    return (hx + hy) / hxy if hxy > 0 else 0.0


# ---------------------------------------------------------------------------
# Capa OpenGL: contexto offscreen compartido por alineacion y fusion
# ---------------------------------------------------------------------------

class ContextoGPU:
    """Contexto OpenGL offscreen (headless, GLFW) con dos programas de
    shaders: 'transformar' (rotacion + traslacion rigida, Tarea 9) y
    'fusionar' (regla de fusion de coeficientes wavelet, Tarea 10)."""

    def __init__(self):
        if not glfw.init():
            raise RuntimeError("No se pudo inicializar GLFW")
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        self.ventana = glfw.create_window(64, 64, "offscreen-tarea10", None, None)
        if not self.ventana:
            glfw.terminate()
            raise RuntimeError("No se pudo crear el contexto OpenGL (ventana oculta)")
        glfw.make_context_current(self.ventana)

        print("Contexto OpenGL creado:")
        print("  GL_VERSION  :", glGetString(GL_VERSION).decode())
        print("  GL_RENDERER :", glGetString(GL_RENDERER).decode())

        self.prog_transformar = self._crear_programa(FRAGMENT_SRC_TRANSFORMAR)
        self.loc_t_angulo = glGetUniformLocation(self.prog_transformar, "uAngulo")
        self.loc_t_traslacion = glGetUniformLocation(self.prog_transformar, "uTraslacionNDC")
        self.loc_t_tex = glGetUniformLocation(self.prog_transformar, "uTex")

        self.prog_fusionar = self._crear_programa(FRAGMENT_SRC_FUSIONAR)
        self.loc_f_angulo = glGetUniformLocation(self.prog_fusionar, "uAngulo")
        self.loc_f_traslacion = glGetUniformLocation(self.prog_fusionar, "uTraslacionNDC")
        self.loc_f_a = glGetUniformLocation(self.prog_fusionar, "uA")
        self.loc_f_b = glGetUniformLocation(self.prog_fusionar, "uB")
        self.loc_f_modo = glGetUniformLocation(self.prog_fusionar, "uModo")
        self.loc_f_wa = glGetUniformLocation(self.prog_fusionar, "uWA")
        self.loc_f_wb = glGetUniformLocation(self.prog_fusionar, "uWB")

        self._crear_quad()

    @staticmethod
    def _compilar_shader(src, tipo):
        sh = glCreateShader(tipo)
        glShaderSource(sh, src)
        glCompileShader(sh)
        if not glGetShaderiv(sh, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(sh).decode())
        return sh

    def _crear_programa(self, fragment_src):
        vs = self._compilar_shader(VERTEX_SRC, GL_VERTEX_SHADER)
        fs = self._compilar_shader(fragment_src, GL_FRAGMENT_SHADER)
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
    def _subir_textura(arr):
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        h, w = arr.shape
        glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, w, h, 0, GL_RED, GL_FLOAT,
                     np.ascontiguousarray(arr, dtype=np.float32))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        return tex

    @staticmethod
    def _crear_destino(w, h):
        tex_dst = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_dst)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, w, h, 0, GL_RED, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex_dst, 0)
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("FBO incompleto")
        return fbo, tex_dst

    def _dibujar_y_leer(self, w, h):
        glViewport(0, 0, w, h)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        datos = glReadPixels(0, 0, w, h, GL_RED, GL_FLOAT)
        arr = np.frombuffer(datos, dtype=np.float32).reshape(h, w).copy()
        return np.flipud(arr)

    # -- Paso A (Tarea 9): transformacion rigida ----------------------------
    def transformar(self, arr_movil, angulo, tx_ndc, ty_ndc):
        """Aplica T(angulo,dx,dy) a 'arr_movil' y regresa el resultado
        remuestreado sobre una malla del mismo tamano (equivalente a
        sitk.Resample, pero ejecutado en GPU)."""
        h, w = arr_movil.shape
        tex_mov = self._subir_textura(arr_movil)
        fbo, tex_dst = self._crear_destino(w, h)

        glUseProgram(self.prog_transformar)
        glUniform1f(self.loc_t_angulo, float(angulo))
        glUniform2f(self.loc_t_traslacion, float(tx_ndc), float(ty_ndc))
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex_mov)
        glUniform1i(self.loc_t_tex, 0)

        resultado = self._dibujar_y_leer(w, h)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDeleteFramebuffers(1, [fbo])
        glDeleteTextures([tex_mov, tex_dst])
        return resultado

    # -- Paso B (Tarea 10): fusion de coeficientes wavelet -------------------
    def fusionar(self, a, b, modo, w_a=0.5, w_b=0.5):
        """Combina, pixel a pixel y en GPU, dos sub-bandas wavelet del mismo
        tamano (coeficientes de aproximacion o de detalle) usando la regla
        indicada por 'modo' (MAX_ABS, PROMEDIO, PRIORIDAD_MRI, PRIORIDAD_PET)."""
        assert a.shape == b.shape
        h, w = a.shape
        tex_a = self._subir_textura(a)
        tex_b = self._subir_textura(b)
        fbo, tex_dst = self._crear_destino(w, h)

        glUseProgram(self.prog_fusionar)
        glUniform1f(self.loc_f_angulo, 0.0)
        glUniform2f(self.loc_f_traslacion, 0.0, 0.0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex_a)
        glUniform1i(self.loc_f_a, 0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, tex_b)
        glUniform1i(self.loc_f_b, 1)
        glUniform1i(self.loc_f_modo, modo)
        glUniform1f(self.loc_f_wa, float(w_a))
        glUniform1f(self.loc_f_wb, float(w_b))

        resultado = self._dibujar_y_leer(w, h)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDeleteFramebuffers(1, [fbo])
        glDeleteTextures([tex_a, tex_b, tex_dst])
        return resultado

    def cerrar(self):
        glfw.destroy_window(self.ventana)
        glfw.terminate()


# ---------------------------------------------------------------------------
# Paso A: Alineacion rigida PET -> MRI (principios de la Tarea 9)
# ---------------------------------------------------------------------------

def alinear_pet_sobre_mri(mri, pet, gpu):
    """Registro rigido (rotacion + traslacion) de PET sobre MRI, igual
    pipeline que 'Tarea 9.py': T inicial por centro de masa, Informacion
    Mutua Normalizada como medida de similitud, optimizador Powell, y la
    transformacion ejecutada en GPU en cada evaluacion de la metrica."""
    cx_r, cy_r = centro_de_masa(mri)
    cx_t, cy_t = centro_de_masa(pet)
    tam = mri.shape[0]
    tx0 = 2.0 * (cx_r - cx_t) / tam
    ty0 = -2.0 * (cy_r - cy_t) / tam
    params0 = np.array([0.0, tx0, ty0])

    def costo(params):
        angulo, tx, ty = params
        warp = gpu.transformar(pet, angulo, tx, ty)
        return -imn_alineacion(mri, warp)

    cotas = [(-0.35, 0.35), (-0.5, 0.5), (-0.5, 0.5)]
    print("\nPaso A: alineacion rigida PET -> MRI (IMN + Powell, GPU)")
    resultado = minimize(costo, params0, method="Powell", bounds=cotas,
                          options={"maxiter": 200, "xtol": 1e-3, "ftol": 1e-5})

    angulo_f, tx_f, ty_f = resultado.x
    pet_inicial = gpu.transformar(pet, *params0)
    pet_alineado = gpu.transformar(pet, angulo_f, tx_f, ty_f)

    print(f"  Angulo de rotacion  : {np.degrees(angulo_f):.2f} grados")
    print(f"  Traslacion (dx, dy) : ({tx_f * tam / 2:.1f}, {ty_f * tam / 2:.1f}) px")
    print(f"  IMN antes / despues : {imn_alineacion(mri, pet_inicial):.4f} / "
          f"{imn_alineacion(mri, pet_alineado):.4f}")
    return pet_alineado, pet_inicial


def figura_alineacion(mri, pet_original, pet_inicial, pet_alineado, out_path):
    dif_antes = np.abs(mri - pet_inicial)
    dif_despues = np.abs(mri - pet_alineado)
    fig, ejes = plt.subplots(2, 3, figsize=(12, 8))
    ejes[0, 0].imshow(mri, cmap="gray"); ejes[0, 0].set_title("MRI (referencia)")
    ejes[0, 1].imshow(pet_original, cmap="hot"); ejes[0, 1].set_title("PET original")
    ejes[0, 2].imshow(pet_alineado, cmap="hot"); ejes[0, 2].set_title("PET alineado")
    ejes[1, 0].imshow(dif_antes, cmap="gray")
    ejes[1, 0].set_title("Diferencia ANTES")
    ejes[1, 1].imshow(dif_despues, cmap="gray")
    ejes[1, 1].set_title("Diferencia DESPUES")
    ejes[1, 2].imshow(mri, cmap="gray")
    ejes[1, 2].imshow(pet_alineado, cmap="hot", alpha=0.45)
    ejes[1, 2].set_title("Sobreposicion MRI + PET")
    for fila in ejes:
        for ax in fila:
            ax.axis("off")
    fig.suptitle("Alineación PET -> MRI")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"Figura guardada en: {out_path}")


# ---------------------------------------------------------------------------
# Paso B: Fusion wavelet (Pasos 1-3 de "Proceso de fusion usando wavelets")
# ---------------------------------------------------------------------------

def fusionar_wavelet(mri, pet, gpu, wavelet="db4", escalas=3,
                      regla_detalle=MAX_ABS, w_ll=0.5):
    """Fusiona mri y pet (mismo tamano, ya alineados) con la transformada
    wavelet 'wavelet' descompuesta en 'escalas' niveles. La sub-banda LL se
    fusiona por promedio ponderado (w_ll para MRI, 1-w_ll para PET); las
    sub-bandas de detalle (LH, HL, HH) se fusionan con 'regla_detalle'.
    Ambas reglas se ejecutan en GPU mediante ContextoGPU.fusionar."""
    h, w = mri.shape
    coef_mri = pywt.wavedec2(mri, wavelet=wavelet, level=escalas)
    coef_pet = pywt.wavedec2(pet, wavelet=wavelet, level=escalas)

    cA_fusionado = gpu.fusionar(coef_mri[0], coef_pet[0], PROMEDIO, w_ll, 1.0 - w_ll)

    detalles_fusionados = []
    for (cH_m, cV_m, cD_m), (cH_p, cV_p, cD_p) in zip(coef_mri[1:], coef_pet[1:]):
        cH_f = gpu.fusionar(cH_m, cH_p, regla_detalle)
        cV_f = gpu.fusionar(cV_m, cV_p, regla_detalle)
        cD_f = gpu.fusionar(cD_m, cD_p, regla_detalle)
        detalles_fusionados.append((cH_f, cV_f, cD_f))

    coef_fusionado = [cA_fusionado] + detalles_fusionados
    fusionada = pywt.waverec2(coef_fusionado, wavelet=wavelet)
    fusionada = fusionada[:h, :w]
    return np.clip(fusionada, 0.0, 1.0)


# ---------------------------------------------------------------------------
# Metricas de calidad (ver diapositiva "Tabla comparativa" / Table 4 del PDF)
# ---------------------------------------------------------------------------

def entropia(img, bins=256):
    img_u8 = np.clip(img * 255.0, 0, 255).astype(np.uint8)
    hist, _ = np.histogram(img_u8, bins=bins, range=(0, 256))
    p = hist / hist.sum()
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def info_mutua_normalizada(a, b, bins=32):
    a_q = np.clip((a * (bins - 1)).astype(np.int32), 0, bins - 1)
    b_q = np.clip((b * (bins - 1)).astype(np.int32), 0, bins - 1)
    hist2d, _, _ = np.histogram2d(a_q.ravel(), b_q.ravel(), bins=bins,
                                   range=[[0, bins], [0, bins]])
    pxy = hist2d / hist2d.sum()
    px, py = pxy.sum(axis=1), pxy.sum(axis=0)
    nz = pxy > 0
    hxy = -np.sum(pxy[nz] * np.log(pxy[nz]))
    hx = -np.sum(px[px > 0] * np.log(px[px > 0]))
    hy = -np.sum(py[py > 0] * np.log(py[py > 0]))
    return (hx + hy) / hxy if hxy > 0 else 0.0


def metricas(fusionada, mri, pet):
    return {
        "SD": fusionada.std() * 100.0,
        "EN": entropia(fusionada),
        "QMI": 0.5 * (info_mutua_normalizada(fusionada, mri)
                       + info_mutua_normalizada(fusionada, pet)),
    }


def imprimir_tabla(filas, nombre_col):
    print(f"\n{nombre_col:<22}{'SD':>10}{'EN':>10}{'QMI':>10}")
    print("-" * 52)
    for nombre, m in filas:
        print(f"{nombre:<22}{m['SD']:>10.2f}{m['EN']:>10.2f}{m['QMI']:>10.3f}")


# ---------------------------------------------------------------------------
# Experimentos de la Tarea 10
# ---------------------------------------------------------------------------

# Una wavelet representativa de cada familia (diapositiva "Tipos de Wavelets comunes")
NOMBRE_FAMILIA = {
    "haar": "Haar",
    "db4": "Daubechies (db4)",
    "sym4": "Symlets (sym4)",
    "bior2.2": "Biortogonal (bior2.2)",
}


def experimento_wavelets(mri, pet, gpu, escalas=3, regla=MAX_ABS):
    wavelets = list(NOMBRE_FAMILIA.keys())
    fig, ejes = plt.subplots(2, 2, figsize=(9, 9))
    filas = []
    for ax, wv in zip(ejes.ravel(), wavelets):
        fusionada = fusionar_wavelet(mri, pet, gpu, wavelet=wv, escalas=escalas, regla_detalle=regla)
        m = metricas(fusionada, mri, pet)
        filas.append((NOMBRE_FAMILIA[wv], m))
        ax.imshow(fusionada, cmap="hot")
        ax.set_title(f"{NOMBRE_FAMILIA[wv]}")
        ax.axis("off")
    fig.suptitle(f"Comparación por tipo de Wavelet (escalas={escalas}, regla={NOMBRE_REGLA[regla]})")
    fig.tight_layout()
    out_path = os.path.join(BASE_DIR, "01_comparacion_wavelets.png")
    fig.savefig(out_path, dpi=150)
    print(f"Figura guardada en: {out_path}")
    imprimir_tabla(filas, "Wavelet")
    return filas


def experimento_escalas(mri, pet, gpu, wavelet="db4", regla=MAX_ABS):
    niveles = [1, 2, 3, 4, 5]
    fig, ejes = plt.subplots(1, 5, figsize=(15, 4))
    filas = []
    for ax, n in zip(ejes, niveles):
        fusionada = fusionar_wavelet(mri, pet, gpu, wavelet=wavelet, escalas=n, regla_detalle=regla)
        m = metricas(fusionada, mri, pet)
        filas.append((f"{n} escala(s)", m))
        ax.imshow(fusionada, cmap="hot")
        ax.set_title(f"{n} escala(s)\nSD={m['SD']:.1f} EN={m['EN']:.2f}")
        ax.axis("off")
    fig.suptitle(f"Comparación por número de escalas (wavelet={wavelet}, regla={NOMBRE_REGLA[regla]})")
    fig.tight_layout()
    out_path = os.path.join(BASE_DIR, "02_comparacion_escalas.png")
    fig.savefig(out_path, dpi=150)
    print(f"Figura guardada en: {out_path}")
    imprimir_tabla(filas, "Escalas")
    return filas


def experimento_reglas(mri, pet, gpu, wavelet="db4", escalas=3):
    reglas = [MAX_ABS, PROMEDIO, PRIORIDAD_MRI, PRIORIDAD_PET]
    fig, ejes = plt.subplots(2, 2, figsize=(9, 9))
    filas = []
    for ax, r in zip(ejes.ravel(), reglas):
        fusionada = fusionar_wavelet(mri, pet, gpu, wavelet=wavelet, escalas=escalas, regla_detalle=r)
        m = metricas(fusionada, mri, pet)
        filas.append((NOMBRE_REGLA[r], m))
        ax.imshow(fusionada, cmap="hot")
        ax.set_title(f"{NOMBRE_REGLA[r]}")
        ax.axis("off")
    fig.suptitle(f"Comparación de coeficientes de detalle (wavelet={wavelet}, escalas={escalas})")
    fig.tight_layout()
    out_path = os.path.join(BASE_DIR, "03_comparacion_reglas_coeficientes.png")
    fig.savefig(out_path, dpi=150)
    print(f"Figura guardada en: {out_path}")
    imprimir_tabla(filas, "Regla de seleccion")
    return filas


def main():
    mri = cargar_gris(MRI_PATH)
    pet_original = cargar_gris(PET_PATH)
    if mri.shape != pet_original.shape:
        pet_original = cv2.resize(pet_original, (mri.shape[1], mri.shape[0]))

    gpu = ContextoGPU()
    try:
        # --- Paso A: alinear PET sobre MRI (principios de la Tarea 9) ------
        pet_alineado, pet_inicial = alinear_pet_sobre_mri(mri, pet_original, gpu)
        figura_alineacion(mri, pet_original, pet_inicial, pet_alineado,
                           os.path.join(BASE_DIR, "00_alineacion.png"))

        # --- Paso B: experimentos de fusion wavelet (Tarea 10) -------------
        experimento_wavelets(mri, pet_alineado, gpu)
        experimento_escalas(mri, pet_alineado, gpu)
        experimento_reglas(mri, pet_alineado, gpu)
    finally:
        gpu.cerrar()

    plt.show()


if __name__ == "__main__":
    main()
