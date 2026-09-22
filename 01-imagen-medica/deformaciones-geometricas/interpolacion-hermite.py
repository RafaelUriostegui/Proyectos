"""
Tarea 7 – Interpolación Hermite para relleno de huecos post-deformación
========================================================================
La tarea anterior aplicó una deformación geométrica (forward mapping)
que dejó huecos en la imagen resultante. Aquí se integra la interpolación
Hermite del Ejemplo 3_1.c para rellenar esos huecos.

Uso:
    python tarea7.py                        # imagen sintética de prueba
    python tarea7.py imagen.png             # imagen propia
    python tarea7.py imagen.png 20 2.0      # amplitud=20, frecuencia=2.0
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ─────────────────────────────────────────────────────────────────────────────
# Carga / imagen de prueba
# ─────────────────────────────────────────────────────────────────────────────

def cargar_imagen(ruta, tam=256):
    img = Image.open(ruta).convert('L')
    return np.array(img.resize((tam, tam), Image.LANCZOS), dtype=np.uint8)


def imagen_prueba(tam=256):
    """Círculo con textura interna (simula corte de cabeza MRI)."""
    y, x = np.meshgrid(np.arange(tam), np.arange(tam), indexing='ij')
    cx, cy, r = tam // 2, tam // 2, tam // 3
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2).astype(np.float32)
    base = np.where(dist < r, 180.0 * (1.0 - dist / r), 0.0)
    textura = 40.0 * np.abs(np.sin(8 * np.pi * y / tam))
    img = np.clip(base + textura * (base > 0), 0, 255).astype(np.uint8)
    return img


# ─────────────────────────────────────────────────────────────────────────────
# Deformación (tarea anterior) – forward mapping sinusoidal
# ─────────────────────────────────────────────────────────────────────────────

def deformar_forward(imagen, amplitud=20.0, frecuencia=2.0):
    """
    Mapeado hacia adelante (forward mapping):
        Δx(y) = amplitud · sin(2π · frecuencia · y / H)

    Cada píxel se desplaza horizontalmente según su fila y.
    El mapeado hacia adelante deja huecos (valor 0) donde ningún
    píxel del original "aterriza".
    """
    H, W = imagen.shape
    salida = np.zeros_like(imagen)

    # Precalcular desplazamiento por fila (vectorizado)
    filas = np.arange(H)
    dx = np.round(amplitud * np.sin(2 * np.pi * frecuencia * filas / H)).astype(int)

    for y in range(H):
        xs = np.arange(W)
        nxs = xs + dx[y]
        validos = (nxs >= 0) & (nxs < W)
        salida[y, nxs[validos]] = imagen[y, xs[validos]]

    return salida


# ─────────────────────────────────────────────────────────────────────────────
# Interpolación Hermite  (Ejemplo 3_1.c traducido a Python)
# ─────────────────────────────────────────────────────────────────────────────

def interpola_hermite(imagen, R1=1.0, R4=-1.0, paso=2):
    """
    Rellena huecos (valor < 10) en el eje x con interpolación Hermite.

    Traducción directa del Ejemplo 3_1.c:
    ─────────────────────────────────────
    Funciones de mezcla:
        B1(t) =  2t³ - 3t² + 1    peso de P1 (punto de inicio)
        B2(t) = -2t³ + 3t²        peso de P4 (punto de fin)
        B3(t) =  t³ - 2t² + t     peso de R1 (tangente inicial)
        B4(t) =  t³ - t²          peso de R4 (tangente final)

    Q(t) = B1·P1 + B2·P4 + B3·R1 + B4·R4,  con t ∈ [0, 1)

    Parámetros
    ----------
    imagen : ndarray uint8   imagen con huecos (valor < 10)
    R1, R4 : float           vectores tangentes en P1 y P4
                             (controlan la forma de la curva en los extremos)
    paso   : int             número de píxeles a interpolar por hueco
    """
    H, W = imagen.shape
    ima = imagen.copy().astype(np.float32)   # operación in-place (igual que C)

    for y in range(H):
        for x in range(1, W - paso):
            if ima[y, x] < 10:                          # hueco detectado
                P1 = ima[y, x - 1]
                idx_P4 = x + paso - 1
                P4 = ima[y, idx_P4] if idx_P4 < W else ima[y, W - 1]

                i = 0
                for t in np.arange(0.0, 1.0, 1.0 / paso):
                    B1 =  2*t**3 - 3*t**2 + 1
                    B2 = -2*t**3 + 3*t**2
                    B3 =    t**3 - 2*t**2 + t
                    B4 =    t**3 - t**2

                    gris = B1*P1 + B2*P4 + B3*R1 + B4*R4
                    pos = x - 1 + i
                    if 0 <= pos < W:
                        ima[y, pos] = float(np.clip(round(gris), 0, 255))
                    i += 1

    return ima.astype(np.uint8)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Argumentos de línea de comandos
    ruta      = sys.argv[1] if len(sys.argv) > 1 else None
    amplitud  = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
    frecuencia = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

    # ── Cargar imagen ────────────────────────────────────────────────────────
    if ruta and os.path.exists(ruta):
        original = cargar_imagen(ruta)
        print(f"Imagen cargada: {ruta}")
    else:
        original = imagen_prueba()
        print("Usando imagen sintética de prueba (256×256).")

    print(f"Dimensiones: {original.shape}  |  Rango: [{original.min()}, {original.max()}]")

    # ── Deformar (genera huecos) ─────────────────────────────────────────────
    print(f"\nDeformando con forward mapping sinusoidal  "
          f"(amplitud={amplitud}, frecuencia={frecuencia})…")
    deformada = deformar_forward(original, amplitud=amplitud, frecuencia=frecuencia)

    huecos = int((deformada < 10).sum())
    total  = original.size
    print(f"Huecos generados: {huecos} px  ({100.0 * huecos / total:.1f} %)")

    # ── Interpolar con diferentes configuraciones ────────────────────────────
    configuraciones = [
        dict(paso=2, R1= 1.0, R4= -1.0),
        dict(paso=3, R1= 1.0, R4= -1.0),
        dict(paso=2, R1= 5.0, R4= -5.0),
        dict(paso=3, R1=15.0, R4=-15.0),
    ]

    resultados = []
    for cfg in configuraciones:
        etiqueta = f"paso={cfg['paso']}, R1={cfg['R1']}, R4={cfg['R4']}"
        print(f"  Interpolando: {etiqueta}…")
        res = interpola_hermite(deformada, **cfg)
        resultados.append((etiqueta, res))

    # ── Visualizar ───────────────────────────────────────────────────────────
    n = 2 + len(resultados)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 5))

    axes[0].imshow(original,  cmap='gray', vmin=0, vmax=255)
    axes[0].set_title('Original')
    axes[0].axis('off')

    axes[1].imshow(deformada, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title(f'Deformada\n({huecos} huecos, {100.0*huecos/total:.1f}%)')
    axes[1].axis('off')

    for i, (etiqueta, img) in enumerate(resultados):
        axes[2 + i].imshow(img, cmap='gray', vmin=0, vmax=255)
        axes[2 + i].set_title(f'Hermite\n{etiqueta}')
        axes[2 + i].axis('off')

    plt.suptitle('Tarea 7 – Interpolación Hermite para relleno de huecos',
                 fontsize=13, y=1.02)
    plt.tight_layout()

    archivo_salida = 'tarea7_resultado.png'
    plt.savefig(archivo_salida, dpi=150, bbox_inches='tight')
    print(f"\nResultado guardado: {archivo_salida}")
    plt.show()

    # ── Guardar imagen deformada e interpolada por separado ──────────────────
    Image.fromarray(deformada).save('tarea7_deformada.png')
    Image.fromarray(resultados[0][1]).save('tarea7_interpolada_paso2.png')
    Image.fromarray(resultados[1][1]).save('tarea7_interpolada_paso3.png')
    print("Guardadas: tarea7_deformada.png, tarea7_interpolada_paso2.png, "
          "tarea7_interpolada_paso3.png")


if __name__ == '__main__':
    main()
