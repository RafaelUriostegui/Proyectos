"""
Tarea 8 - Cortes oblicuos de pila MRI (RMHEA109S)
==================================================
La pila RMHEA109S contiene 109 cortes sagitales de cabeza humana de
resonancia magnetica (256x256 px cada uno, 1 corte/pixel en z).

Se simula un corte no ortogonal al angulo theta deseado, obteniendo una
imagen de 256x256 mediante interpolacion bilineal/trilineal.

Geometria del corte oblicuo (plano x-z):
    Para cada pixel (fila r, columna c) de la salida 256x256:
        y_vol = r * (ny-1)/(H-1)               <- eje vertical sin cambio
        x_vol = c * cos(theta) * (nx-1)/(W-1)  <- avance horizontal
        z_vol = c * sin(theta) * (nz-1)/(W-1)  <- avance en profundidad

    theta=0  -> corte paralelo a eje x  (= corte sagital z=0)
    theta=45 -> diagonal, combina x y z por igual
    theta=90 -> perpendicular a x (barre todos los 109 slices en z)

Uso:
    python tarea8.py                   # volumen de prueba, theta=30
    python tarea8.py RMHEA109S         # directorio con imagenes, theta=30
    python tarea8.py RMHEA109S 45      # theta=45 grados
    python tarea8.py volumen.raw 30    # archivo raw unico (109x256x256 bytes)
"""

import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ---------------------------------------------------------------------------
# Carga del volumen
# ---------------------------------------------------------------------------

def cargar_directorio(ruta, nz=109, ny=256, nx=256):
    """Carga pila de imagenes desde un directorio (PNG, PGM, BMP, JPG, RAW)."""
    patrones = ['*.png', '*.pgm', '*.bmp', '*.jpg', '*.jpeg', '*.tif', '*.raw']
    archivos = []
    for p in patrones:
        archivos += glob.glob(os.path.join(ruta, p))
    archivos = sorted(archivos)[:nz]

    if not archivos:
        raise FileNotFoundError("No se encontraron imagenes en '" + ruta + "'")

    print("  Encontrados " + str(len(archivos)) + " archivos en '" + ruta + "'")
    cortes = []
    for f in archivos:
        if f.lower().endswith('.raw'):
            datos = np.fromfile(f, dtype=np.uint8)
            corte = datos[:nx * ny].reshape(ny, nx)
        else:
            img = Image.open(f).convert('L')
            if img.size != (nx, ny):
                img = img.resize((nx, ny), Image.LANCZOS)
            corte = np.array(img, dtype=np.uint8)
        cortes.append(corte)

    return np.array(cortes, dtype=np.uint8)   # (nz, ny, nx)


def cargar_raw_unico(ruta, nz=109, ny=256, nx=256):
    """Carga volumen desde un unico archivo binario raw uint8."""
    datos = np.fromfile(ruta, dtype=np.uint8)
    esperado = nz * ny * nx
    if datos.size == esperado:
        print("  Archivo raw '" + ruta + "' -> shape (" + str(nz) + "," + str(ny) + "," + str(nx) + ")")
        return datos.reshape(nz, ny, nx)
    raise ValueError("Tamano inesperado: " + str(datos.size) + " bytes (esperado " + str(esperado) + ")")


def cargar_volumen(ruta, nz=109, ny=256, nx=256):
    """Intenta cargar el volumen desde directorio o archivo raw."""
    if os.path.isdir(ruta):
        return cargar_directorio(ruta, nz, ny, nx)
    if os.path.isfile(ruta):
        return cargar_raw_unico(ruta, nz, ny, nx)
    raise FileNotFoundError("No se encontro '" + ruta + "'")


def volumen_prueba(nz=109, ny=256, nx=256):
    """Volumen sintetico (elipsoide con textura) para pruebas sin dataset real."""
    print("  Generando volumen de prueba (elipsoide sintetico)...")
    z = np.linspace(-1, 1, nz)[:, None, None]
    y = np.linspace(-1, 1, ny)[None, :, None]
    x = np.linspace(-1, 1, nx)[None, None, :]

    r2 = (x / 0.80)**2 + (y / 0.90)**2 + (z / 0.65)**2
    exterior = np.where((r2 >= 0.85) & (r2 < 1.0),
                        150.0 * (1.0 - (r2 - 0.85) / 0.15), 0.0)
    interior = np.where(r2 < 0.85,
                        100.0 * (1.0 - r2**0.5) *
                        (1 + 0.4 * np.sin(6 * np.pi * z) * np.cos(4 * np.pi * x)), 0.0)
    vol = np.clip(exterior + interior, 0, 255).astype(np.uint8)
    return vol


# ---------------------------------------------------------------------------
# Corte oblicuo con interpolacion
# ---------------------------------------------------------------------------

def corte_oblicuo(volumen, theta_grados, H=256, W=256):
    """
    Genera la imagen H x W del corte oblicuo al angulo theta.

    Intenta usar scipy (rapido); si no esta disponible usa bucles (lento).
    """
    try:
        from scipy.ndimage import map_coordinates
        return _corte_scipy(volumen, theta_grados, H, W)
    except ImportError:
        print("  (scipy no disponible - usando bucles, puede tardar)")
        return _corte_bucles(volumen, theta_grados, H, W)


def _corte_scipy(volumen, theta_grados, H=256, W=256):
    """
    Corte oblicuo con scipy.ndimage.map_coordinates (interpolacion bilineal, orden=1).

    Para cada pixel (r, c) de la imagen de salida H x W:
        y_vol = r * (ny-1)/(H-1)
        x_vol = c * cos(theta) * (nx-1)/(W-1)
        z_vol = c * sin(theta) * (nz-1)/(W-1)

    La interpolacion bilineal permite obtener valores en posiciones
    no enteras del volumen, escalando el resultado a exactamente 256x256.
    """
    from scipy.ndimage import map_coordinates

    nz, ny, nx = volumen.shape
    theta = np.radians(theta_grados)

    # El corte pasa por el CENTRO del volumen (cx, cz) para que theta=0
    # muestre el slice sagital central y theta=90 muestre x=centro.
    # scale_z mapea la misma "distancia" en z que en x, compensando nz < nx.
    cx      = (nx - 1) / 2.0          # centro x = 127.5
    cz      = (nz - 1) / 2.0          # centro z = 54.0
    col_c   = (W  - 1) / 2.0          # columna central de salida = 127.5
    scale_z = (nz - 1) / (nx - 1)     # relacion de aspecto z/x = 108/255

    filas = np.linspace(0, ny - 1, H)
    cols  = np.arange(W, dtype=np.float64)
    R, C  = np.meshgrid(filas, cols, indexing='ij')   # shape (H, W)

    y_coords = R
    x_coords = cx + (C - col_c) * np.cos(theta)
    z_coords = cz + (C - col_c) * np.sin(theta) * scale_z

    # Clampar al rango valido antes de interpolar
    x_coords = np.clip(x_coords, 0, nx - 1)
    z_coords = np.clip(z_coords, 0, nz - 1)

    # map_coordinates necesita coordenadas por eje: [eje0=z, eje1=y, eje2=x]
    coords = np.array([z_coords.ravel(),
                       y_coords.ravel(),
                       x_coords.ravel()])

    vals = map_coordinates(volumen.astype(np.float32), coords,
                           order=1, mode='constant', cval=0.0)
    return vals.reshape(H, W).astype(np.uint8)


def _corte_bucles(volumen, theta_grados, H=256, W=256):
    """Corte oblicuo con bucles explicitos e interpolacion trilineal manual."""
    nz, ny, nx = volumen.shape
    theta   = np.radians(theta_grados)
    cx      = (nx - 1) / 2.0
    cz      = (nz - 1) / 2.0
    col_c   = (W  - 1) / 2.0
    scale_z = (nz - 1) / (nx - 1)
    salida  = np.zeros((H, W), dtype=np.float32)

    for r in range(H):
        y_f = r * (ny - 1) / (H - 1)
        y0 = int(y_f);  y1 = min(y0 + 1, ny - 1)
        dy = y_f - y0

        for c in range(W):
            x_f = float(np.clip(cx + (c - col_c) * np.cos(theta), 0, nx - 1.001))
            z_f = float(np.clip(cz + (c - col_c) * np.sin(theta) * scale_z, 0, nz - 1.001))

            x0 = int(x_f);  x1 = min(x0 + 1, nx - 1)
            z0 = int(z_f);  z1 = min(z0 + 1, nz - 1)
            dx = x_f - x0;  dz = z_f - z0

            salida[r, c] = (
                (1-dz)*(1-dy)*(1-dx)*volumen[z0, y0, x0] +
                (1-dz)*(1-dy)*   dx *volumen[z0, y0, x1] +
                (1-dz)*   dy *(1-dx)*volumen[z0, y1, x0] +
                (1-dz)*   dy *   dx *volumen[z0, y1, x1] +
                   dz *(1-dy)*(1-dx)*volumen[z1, y0, x0] +
                   dz *(1-dy)*   dx *volumen[z1, y0, x1] +
                   dz *   dy *(1-dx)*volumen[z1, y1, x0] +
                   dz *   dy *   dx *volumen[z1, y1, x1]
            )

    return salida.astype(np.uint8)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ruta  = sys.argv[1] if len(sys.argv) > 1 else 'RMHEA109S'
    theta = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0

    print("=== Tarea 8: Cortes oblicuos de MRI ===")
    print("Origen: '" + ruta + "'  |  theta = " + str(theta) + " grados\n")

    # Cargar volumen
    try:
        vol = cargar_volumen(ruta)
    except (FileNotFoundError, ValueError) as e:
        print("AVISO: " + str(e))
        print("Usando volumen sintetico de prueba.")
        vol = volumen_prueba()

    nz, ny, nx = vol.shape
    print("\nVolumen: " + str(vol.shape) +
          "  rango [" + str(vol.min()) + ", " + str(vol.max()) + "]\n")

    # Angulos a generar: 0, theta/2, theta, min(theta*1.5, 90), 90
    angulos_set = {0, int(theta / 2), int(theta),
                   min(int(theta * 1.5), 90), 90}
    angulos = sorted(angulos_set)

    print("Generando cortes para theta in " + str(angulos) + " grados...")
    cortes = {}
    for ang in angulos:
        print("  theta = " + str(ang) + " grados...", end='  ', flush=True)
        cortes[ang] = corte_oblicuo(vol, ang)
        print("OK")

    # Visualizar
    n_col = len(cortes) + 1
    fig, axes = plt.subplots(1, n_col, figsize=(5 * n_col, 5))

    # Referencia: corte sagital central del dataset
    axes[0].imshow(vol[nz // 2], cmap='gray', vmin=0, vmax=255)
    axes[0].set_title('Sagital original\n(slice ' + str(nz // 2) + ')')
    axes[0].axis('off')

    for i, (ang, corte) in enumerate(cortes.items()):
        axes[i + 1].imshow(corte, cmap='gray', vmin=0, vmax=255)
        axes[i + 1].set_title('Corte oblicuo\ntheta=' + str(ang) + ' grados')
        axes[i + 1].axis('off')

    plt.suptitle(
        'Tarea 8 - Cortes oblicuos de MRI con interpolacion bilineal',
        fontsize=12, y=1.01)
    plt.tight_layout()

    archivo_salida = 'tarea8_resultado.png'
    plt.savefig(archivo_salida, dpi=150, bbox_inches='tight')
    print("\nResultado guardado: " + archivo_salida)

    # Guardar cada corte individual como PNG
    for ang, corte in cortes.items():
        nombre = 'corte_oblicuo_theta' + str(ang).zfill(3) + '.png'
        Image.fromarray(corte).save(nombre)
        print("Guardado: " + nombre)

    plt.show()


if __name__ == '__main__':
    main()
