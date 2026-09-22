# Proyectos

**Portafolio de ingeniería biomédica computacional** — Rafael Uriostegui Sánchez

Procesamiento de imagen médica, inteligencia artificial aplicada a diagnóstico, procesamiento digital
de señales biomédicas, métodos numéricos y sistemas embebidos. 23 proyectos desarrollados durante mi
formación en la **UAM**, el **Tecnológico de Monterrey** y la **UNAM**.

> **EN — Computational biomedical engineering portfolio.** 23 projects spanning medical image
> registration and fusion (including a GPU/GLSL implementation of rigid multimodal registration),
> deep learning for neurodegenerative disease diagnosis with Grad-CAM interpretability, biomedical
> digital signal processing (sleep apnea spectral analysis, PCA on radionuclide ventriculography,
> video-based photoplethysmography, analogue and digital filter design validated with SPICE),
> numerical methods, and ESP32/MicroPython embedded systems. Every notebook keeps its outputs, so
> results and figures are visible on GitHub without running anything. Project documentation is in
> Spanish, with an English summary at the top of each README.

---

## Áreas

| | Área | Proyectos | Contenido |
|---|---|---|---|
| 🧠 | **[Imagen médica](01-imagen-medica/)** | 5 | Registro multimodal PET–MRI, fusión wavelet, *reslicing* oblicuo, deformaciones geométricas, visor volumétrico |
| 🤖 | **[IA para diagnóstico](02-ia-diagnostico/)** | 4 | CNN para Alzheimer con Grad-CAM, ML clásico para Parkinson, fuga de datos, aprendizaje no supervisado |
| 📈 | **[Señales biomédicas](03-senales-biomedicas/)** | 8 | Apnea del sueño, ACP en ventriculografía, PPG por video, filtros analógicos y digitales |
| 🔢 | **[Métodos numéricos](04-metodos-numericos/)** | 4 | Integración numérica, descenso por gradiente, perceptrón, interpolación, ajuste por mínimos cuadrados |
| ⚡ | **[Sistemas embebidos](05-sistemas-embebidos/)** | 2 | ESP32/MicroPython: control de NeoPixel y cerradura con PIN |

---

## Proyectos destacados

### [Registro rígido multimodal PET–MRI](01-imagen-medica/registro-pet-mri/)

Alineación de PET sobre MRI resuelta **dos veces para compararlas**: una remuestreando en GPU con un
*shader* GLSL propio y optimizando Información Mutua Normalizada con el método de Powell, y otra con
SimpleITK usando Mattes MI y Regular Step Gradient Descent. La versión GPU ejecuta el paso de
transformación como *fragment shader* en lugar de usar el remuestreador de una librería.

`PyOpenGL` · `GLSL` · `SimpleITK` · `SciPy`

### [CNN para clasificación de Alzheimer + Grad-CAM](02-ia-diagnostico/cnn-alzheimer-gradcam/)

Red convolucional entrenada **desde cero** (sin pesos preentrenados) para separar Alzheimer de
controles sanos sobre MRI, con evaluación completa e interpretabilidad mediante mapas de calor
Grad-CAM que muestran en qué región se apoya cada predicción.

`TensorFlow/Keras` · `scikit-learn` · `Grad-CAM`

### [Fuga de datos en ML médico](02-ia-diagnostico/fuga-datos-ml-medico/)

Demuestra por qué un AUC alto puede ser una ilusión: con varias grabaciones por paciente, una
división aleatoria permite que el modelo memorice firmas individuales. Al repetir el pipeline con
división **por paciente**, aparece el desempeño real frente a pacientes no vistos.

`scikit-learn` · `GroupShuffleSplit` · `XGBoost`

### [Análisis espectral de apnea del sueño](03-senales-biomedicas/apnea-sueno-analisis-espectral/)

Estudio con hipótesis explícita sobre el registro polisomnográfico `slp59m` de PhysioNet: las señales
respiratorias se segmentan por tipo de evento anotado — apnea obstructiva, apnea central, hipopnea y
*arousal* — y se comparan contra ventanas sin evento mediante espectrogramas y distribución de
potencia espectral.

`SciPy` · `PhysioNet/slpdb` · `pandas`

### [Fusión wavelet PET–MRI](01-imagen-medica/fusion-wavelet-pet-mri/)

Fusión multiescala barriendo tres variables: familia wavelet (Haar, Daubechies, Symlets,
Biorthogonal), número de escalas (1–5) y regla de selección de coeficientes de detalle (máximo
absoluto, promedio, prioridad MRI, prioridad PET).

`PyWavelets` · `OpenCV` · `PyOpenGL`

### [ESP32 — Control de NeoPixel](05-sistemas-embebidos/esp32-control-neopixel/)

Firmware por eventos: teclado analógico de cinco botones leído en **un solo pin ADC** por umbrales,
encoder rotatorio con detección de sentido por flanco, antirrebote con temporizador *one-shot* y una
máquina de estados alimentada por cola de eventos. Ninguna rutina de interrupción hace trabajo pesado.

`MicroPython` · `ESP32`

---

## Stack técnico

| Categoría | Herramientas |
|---|---|
| Lenguajes | Python, C, MicroPython, GLSL |
| Cómputo científico | NumPy, SciPy, SymPy, pandas |
| *Machine learning* | TensorFlow/Keras, scikit-learn, XGBoost, imbalanced-learn |
| Imagen médica | SimpleITK, PyWavelets, OpenCV, Pillow |
| Señales biomédicas | MNE, NeuroKit2, WFDB, PySpice |
| Gráficos | PyOpenGL, GLUT/GLFW, shaders GLSL |
| Visualización | Matplotlib, seaborn |
| Embebidos | ESP32, MicroPython, NeoPixel, encoders, ADC |

---

## Notas sobre reproducibilidad

- **Los notebooks conservan sus salidas.** Gráficas, métricas y resultados se ven directamente en
  GitHub sin necesidad de ejecutarlos.
- **Varios notebooks fueron escritos en Google Colab** y cargan datos desde Google Drive con rutas
  tipo `/content/drive/MyDrive/...`. Se dejaron tal cual para no alterar código que no puedo
  reejecutar aquí; cada README indica de dónde proceden sus datos.
- **Los datos incluidos** (`.mat` en las carpetas `datos/`) permiten ejecutar los proyectos que
  dependen de archivos pequeños. Los conjuntos grandes o material propio de cada curso no se
  incluyen: su origen está documentado en el README correspondiente, y cuando son públicos
  (PhysioNet) se enlaza la fuente.
- Cada área tiene su propio `requirements.txt`.

---

## Créditos académicos

Estos proyectos se desarrollaron como prácticas y trabajos de curso. Donde partí de una plantilla o
material proporcionado por un profesor, lo indico explícitamente:

| Curso | Institución | Material de partida |
|---|---|---|
| IA para el diagnóstico de enfermedades neurodegenerativas | Tecnológico de Monterrey | Plantillas de laboratorio del **Dr. Alejandro Santos Díaz** |
| Métodos Computacionales en Ingeniería Biomédica (MCIB) | UAM | Material de clase de **Raquel Valdés** |
| Machine Learning | UNAM | Material del curso |
| Visualización e Imagenología Médica por Computadora (VIMC) | UAM | Enunciados y pilas de imágenes del curso |
| Filtros Analógicos y Digitales (FAyD) | UAM | Enunciados de práctica |
| Procesamiento Digital de Señales Biomédicas | UAM | Enunciados de práctica |
| Señales y Medición (SyM) | UAM | Proyecto libre y proyecto final |

El desarrollo, la implementación, los resultados y el análisis son míos.

---

## Licencia

[MIT](LICENSE) — Rafael Uriostegui Sánchez
