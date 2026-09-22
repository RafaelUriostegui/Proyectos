"""
Tarea 9. Alineacion de imagenes medicas multimodales (PET-MRI) de cabeza humana.

Imagen Referencia (fija):  MRI.png  -> mejor resolucion anatomica
Imagen Objetivo  (movil):  PET.png  -> se alinea sobre la MRI

Medida de similitud : Informacion Mutua de Mattes (IMN) -> apta para multimodalidad
Metodo de optimizacion : Regular Step Gradient Descent (el mismo usado por SimpleITK,
                          ver diapositivas "Regular Step Gradient Descent")
Transformacion       : Rigida 2D (rotacion + traslacion), Euler2DTransform

Al final se grafica la imagen diferencia |f_R - f_T| (diapositiva "Diferencia
Cuadratica Media") antes y despues del registro.
"""

import os

import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PET_PATH = os.path.join(BASE_DIR, "PET.png")
MRI_PATH = os.path.join(BASE_DIR, "MRI.png")
OUT_PATH = os.path.join(BASE_DIR, "resultado_alineacion.png")


def cargar_como_array_float(path):
    """Lee un PNG (color o gris) y lo regresa como arreglo 2D float32 en [0, 1]."""
    img = Image.open(path).convert("L")  # luminancia: el colormap 'hot' del PET
    arr = np.asarray(img, dtype=np.float32)  # es creciente con la intensidad real
    arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    return arr


def a_sitk(arr):
    img = sitk.GetImageFromArray(arr)
    img = sitk.Cast(img, sitk.sitkFloat32)
    return img


def diferencia(fija_arr, movil_arr):
    """Diferencia cuadratica media normalizada, ver diapositiva 8: I = |fR - fT|."""
    return np.abs(fija_arr - movil_arr)


def imprimir_progreso(metodo):
    print(f"  iter {metodo.GetOptimizerIteration():3d}  "
          f"metrica = {metodo.GetMetricValue(): .6f}")


def main():
    # 1. Cargar imagenes como arreglos normalizados -----------------------------
    fr_arr = cargar_como_array_float(MRI_PATH)   # Imagen Referencia
    ft_arr = cargar_como_array_float(PET_PATH)    # Imagen Objetivo

    imagen_referencia = a_sitk(fr_arr)
    imagen_objetivo = a_sitk(ft_arr)

    # 2. Transformacion inicial (alinea centros de masa) ------------------------
    transform_inicial = sitk.CenteredTransformInitializer(
        imagen_referencia,
        imagen_objetivo,
        sitk.Euler2DTransform(),
        sitk.CenteredTransformInitializerFilter.MOMENTS,
    )

    # 3. Configuracion del metodo de registro ------------------------------------
    metodo_registro = sitk.ImageRegistrationMethod()

    # Medida de similitud: Informacion Mutua de Mattes (robusta a multimodalidad)
    metodo_registro.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    metodo_registro.SetMetricSamplingStrategy(metodo_registro.RANDOM)
    metodo_registro.SetMetricSamplingPercentage(0.50, seed=42)  # reproducible

    metodo_registro.SetInterpolator(sitk.sitkLinear)

    # Metodo de optimizacion: Regular Step Gradient Descent
    metodo_registro.SetOptimizerAsRegularStepGradientDescent(
        learningRate=2.0,
        minStep=1e-4,
        numberOfIterations=300,
        gradientMagnitudeTolerance=1e-8,
    )
    metodo_registro.SetOptimizerScalesFromPhysicalShift()

    # Estrategia multi-resolucion para evitar minimos locales
    metodo_registro.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    metodo_registro.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    metodo_registro.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    metodo_registro.SetInitialTransform(transform_inicial, inPlace=False)
    metodo_registro.AddCommand(sitk.sitkIterationEvent,
                                lambda: imprimir_progreso(metodo_registro))

    # 4. Ejecutar el registro -----------------------------------------------------
    print("Iniciando registro rigido PET -> MRI (Mattes MI + Regular Step Gradient Descent)")
    transform_final = metodo_registro.Execute(imagen_referencia, imagen_objetivo)

    print("\nResultado del registro")
    print(f"  Condicion de paro     : {metodo_registro.GetOptimizerStopConditionDescription()}")
    print(f"  Iteraciones           : {metodo_registro.GetOptimizerIteration()}")
    print(f"  Metrica final (Mattes): {metodo_registro.GetMetricValue():.6f}")
    angulo, dx, dy = transform_final.GetParameters()
    print(f"  Angulo de rotacion    : {np.degrees(angulo):.3f} grados")
    print(f"  Traslacion (dx, dy)   : ({dx:.2f}, {dy:.2f}) px")

    # 5. Remuestrear la imagen objetivo (PET) con la transformacion final --------
    objetivo_alineado = sitk.Resample(
        imagen_objetivo,
        imagen_referencia,
        transform_final,
        sitk.sitkLinear,
        0.0,
        imagen_objetivo.GetPixelID(),
    )

    # Tambien se remuestrea con la transformacion inicial (sin optimizar) para
    # poder comparar la imagen diferencia antes/despues del registro.
    objetivo_inicial = sitk.Resample(
        imagen_objetivo,
        imagen_referencia,
        transform_inicial,
        sitk.sitkLinear,
        0.0,
        imagen_objetivo.GetPixelID(),
    )

    objetivo_alineado_arr = sitk.GetArrayFromImage(objetivo_alineado)
    objetivo_inicial_arr = sitk.GetArrayFromImage(objetivo_inicial)

    # 6. Imagenes diferencia -------------------------------------------------------
    dif_antes = diferencia(fr_arr, objetivo_inicial_arr)
    dif_despues = diferencia(fr_arr, objetivo_alineado_arr)

    print(f"\n  |dif| promedio antes del registro    : {dif_antes.mean():.4f}")
    print(f"  |dif| promedio despues del registro  : {dif_despues.mean():.4f}")

    # 7. Graficas -------------------------------------------------------------------
    fig, ejes = plt.subplots(2, 3, figsize=(13, 9))

    ejes[0, 0].imshow(fr_arr, cmap="gray")
    ejes[0, 0].set_title("Imagen Referencia (MRI)")

    ejes[0, 1].imshow(ft_arr, cmap="hot")
    ejes[0, 1].set_title("Imagen Objetivo (PET) original")

    ejes[0, 2].imshow(objetivo_alineado_arr, cmap="hot")
    ejes[0, 2].set_title("PET alineado (resultado)")

    ejes[1, 0].imshow(dif_antes, cmap="gray")
    ejes[1, 0].set_title(f"Diferencia ANTES\nmedia={dif_antes.mean():.4f}")

    ejes[1, 1].imshow(dif_despues, cmap="gray")
    ejes[1, 1].set_title(f"Diferencia DESPUES (final)\nmedia={dif_despues.mean():.4f}")

    ejes[1, 2].imshow(fr_arr, cmap="gray")
    ejes[1, 2].imshow(objetivo_alineado_arr, cmap="hot", alpha=0.45)
    ejes[1, 2].set_title("Sobreposicion MRI + PET alineado")

    for fila in ejes:
        for ax in fila:
            ax.axis("off")

    fig.suptitle(
        "Alineacion rigida PET-MRI  |  Mattes Mutual Information + "
        "Regular Step Gradient Descent",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=150)
    print(f"\nFigura guardada en: {OUT_PATH}")
    plt.show()


if __name__ == "__main__":
    main()
