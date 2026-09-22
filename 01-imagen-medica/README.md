# Imagen médica

> **EN —** Medical image processing and visualisation: multimodal registration, wavelet fusion,
> oblique reslicing, geometric deformations and volumetric viewing — combining Python with OpenGL and
> custom GLSL shaders.

Procesamiento y visualización de imagen médica con Python, OpenGL y *shaders* GLSL.

| Proyecto | Descripción | Stack |
|---|---|---|
| [Registro rígido PET–MRI](registro-pet-mri/) | Registro multimodal en dos implementaciones: *shader* GLSL + Información Mutua Normalizada + Powell, contra SimpleITK + Mattes MI + Regular Step Gradient Descent | PyOpenGL, GLSL, SimpleITK, SciPy |
| [Fusión wavelet PET–MRI](fusion-wavelet-pet-mri/) | Fusión multiescala comparando 4 familias wavelet, 5 escalas y 4 reglas de selección de coeficientes | PyWavelets, OpenCV, PyOpenGL |
| [Cortes oblicuos MRI](reslicing-oblicuo-mri/) | Cortes no ortogonales sobre pila de 109 cortes sagitales con interpolación trilineal | NumPy, Matplotlib |
| [Deformaciones geométricas](deformaciones-geometricas/) | Möbius recursiva, deformación Castel & Angel e interpolación de Hermite para relleno de huecos | PyOpenGL, NumPy |
| [Visor volumétrico `.raw`](visor-volumetrico-raw/) | Visor de pilas crudas con detección automática de bytes/píxel y rotación sobre el centro de masa | PyOpenGL, NumPy |

## Instalación

```bash
pip install -r requirements.txt
```
