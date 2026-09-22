# Cortes oblicuos sobre volumen MRI

> **EN —** Generates arbitrary non-orthogonal slices through a stack of 109 sagittal MRI head images
> using trilinear interpolation. For each output pixel the sampling point is computed in volume
> coordinates from the requested angle, then interpolated from the eight surrounding voxels.

## Objetivo

Dada una pila de 109 cortes sagitales de 256×256 px, obtener un corte a un ángulo θ **arbitrario**
respecto a los ejes del volumen — algo que no se consigue simplemente eligiendo un índice de corte.

## Método

Para cada píxel (fila `r`, columna `c`) de la imagen de salida:

```
y_vol = r · (ny−1)/(H−1)              # eje vertical sin cambio
x_vol = c · cos(θ) · (nx−1)/(W−1)     # avance horizontal
z_vol = c · sin(θ) · (nz−1)/(W−1)     # avance en profundidad
```

- `θ = 0°` → corte sagital convencional
- `θ = 45°` → combina x y z por igual
- `θ = 90°` → perpendicular, barre los 109 cortes

El muestreo cae entre vóxeles, así que se interpola **trilinealmente** sobre los ocho vecinos.

## Stack

`NumPy` · `Matplotlib` · `Pillow`

## Cómo ejecutar

El script genera un **volumen sintético de prueba** si no se le pasa ningún dato, así que corre sin
descargas previas:

```bash
python reslicing-oblicuo-mri.py                # volumen sintético, θ=30°
python reslicing-oblicuo-mri.py RMHEA109S      # directorio con la pila de imágenes
python reslicing-oblicuo-mri.py RMHEA109S 45   # θ=45°
python reslicing-oblicuo-mri.py volumen.raw 30 # archivo .raw único (109×256×256 bytes)
```

> La pila original `RMHEA109S` es material del curso y no se incluye en el repositorio.

---

<sub>Visualización e Imagenología Médica por Computadora (VIMC) — UAM, trimestre 26-P.</sub>
