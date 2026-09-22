# Deformaciones geométricas e interpolación

> **EN —** Three geometric image-transformation exercises: a recursive modified Möbius transform, the
> Castel & Angel radial deformation, and Hermite interpolation used to fill the holes that forward
> mapping leaves behind.

## Los tres scripts

### 1. [`transformacion-mobius.py`](transformacion-mobius.py)

Transformación de **Möbius** modificada y aplicada de forma **recursiva** (orden 30) sobre cortes de
imagen médica en formato `.raw`, con visualización en OpenGL. Los coeficientes complejos `a, b, c, d`
controlan la deformación resultante.

### 2. [`deformacion-castel-angel.py`](deformacion-castel-angel.py)

Deformación radial **Castel & Angel**: el desplazamiento de cada píxel depende de su distancia
normalizada `λ` al centro de un círculo de radio `r`, atenuada por un exponente `α`. Produce un efecto
de lente sobre la región de interés.

### 3. [`interpolacion-hermite.py`](interpolacion-hermite.py)

Resuelve un problema real del *forward mapping*: al deformar una imagen empujando píxeles origen →
destino, quedan **huecos** sin asignar. Este script aplica una deformación sinusoidal y luego rellena
esos huecos con **interpolación de Hermite**, que preserva la continuidad de la derivada y evita los
artefactos escalonados de una interpolación lineal.

## Stack

`PyOpenGL` · `NumPy` · `Matplotlib` · `Pillow`

## Cómo ejecutar

`interpolacion-hermite.py` incluye una imagen sintética de prueba (un círculo con textura que simula
un corte de cabeza MRI), así que funciona sin datos externos:

```bash
python interpolacion-hermite.py                     # imagen sintética
python interpolacion-hermite.py imagen.png          # imagen propia
python interpolacion-hermite.py imagen.png 20 2.0   # amplitud=20, frecuencia=2.0

python transformacion-mobius.py       # pide la ruta de un .raw por consola
python deformacion-castel-angel.py    # pide la ruta de un .raw por consola
```

---

<sub>Visualización e Imagenología Médica por Computadora (VIMC) — UAM, trimestre 26-P.</sub>
