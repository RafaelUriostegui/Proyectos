# Visor de pilas volumétricas `.raw`

> **EN —** An OpenGL viewer for raw medical image stacks that auto-detects bytes-per-pixel from the
> file size, plus a second program that rotates the whole stack about its centre of mass.

## Los dos programas

### 1. [`visor-pila-raw.py`](visor-pila-raw.py)

Carga una pila de imágenes médicas en formato **crudo** (`.raw`, sin cabecera) y la recorre corte por
corte en una ventana OpenGL.

Detalles que resuelve:

- **Detección automática de bytes por píxel**: divide el tamaño real del archivo entre el número
  total de píxeles; si da 1 (`uint8`) o 2 (`uint16`) lo usa, si no, pide el valor al usuario.
- **Normalización de rutas**: limpia las comillas que pega el Explorador de Windows al copiar una
  ruta, normaliza separadores y resuelve rutas relativas.
- **Normalización de intensidad** con el máximo global del volumen, para que el brillo no salte entre
  cortes.

### 2. [`rotacion-centro-de-masa.py`](rotacion-centro-de-masa.py)

Rota la pila completa alrededor de su **centro de masa** (no del centro geométrico de la imagen),
calculado a partir de las intensidades. Anima la rotación con un temporizador GLUT.

## Stack

`PyOpenGL` · `NumPy`

## Cómo ejecutar

```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
python visor-pila-raw.py             # pide ruta y dimensiones por consola
python rotacion-centro-de-masa.py
```

> Las pilas `.raw` son material del curso y no se incluyen en el repositorio. El formato esperado es
> `tamZ` cortes consecutivos de `tamY × tamX` píxeles, sin cabecera.

---

<sub>Visualización e Imagenología Médica por Computadora (VIMC) — UAM, trimestre 26-P.</sub>
