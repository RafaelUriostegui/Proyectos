# Interpolación: splines y *morphing* de imágenes

> **EN —** Interpolation from two angles: cubic and variable-order splines over 1-D data, and the
> visible effect that the choice of interpolation method has on image rescaling and morphing.

## Los dos notebooks

### 1. [`splines-interpolacion.ipynb`](splines-interpolacion.ipynb)

- **Interpolación spline cúbica** directa.
- **Splines de orden variable** y comparación del resultado según el orden elegido.

### 2. [`interpolacion-morphing-imagenes.ipynb`](interpolacion-morphing-imagenes.ipynb)

Preprocesamiento de imágenes digitales aplicado a imagen médica (IRM):

- Lectura de la imagen y consulta de sus propiedades.
- **Escalamiento de intensidad** e interpretación de los parámetros.
- **Redimensionamiento** con distintos métodos de interpolación, comparando la calidad resultante.
- Efecto del **morphing** según la interpolación utilizada.

## Stack

`SciPy` (`interpolate`) · `OpenCV` · `NumPy` · `Matplotlib`

## Cómo ejecutar

```bash
pip install numpy scipy opencv-python matplotlib
jupyter notebook splines-interpolacion.ipynb
```

> `interpolacion-morphing-imagenes.ipynb` fue escrito en Colab y carga `IRM2.jpg` desde Google Drive
> (material del curso, no incluido). Las salidas guardadas muestran todas las comparaciones.

---

<sub>Práctica 3 de Métodos Computacionales en Ingeniería Biomédica (MCIB) — UAM, trimestre 26-P. Basada en «PDI. Taller 2: Preprocesamiento de imágenes digitales».</sub>
