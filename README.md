# Computational Biomedical Engineering Portfolio

**Rafael Uriostegui Sánchez**  
Biomedical Engineering student · Medical Imaging · Biomedical AI · Biosignal Processing

Portafolio académico con **23 proyectos** desarrollados durante mi formación en la **UAM**, el **Tecnológico de Monterrey** y la **UNAM**. El énfasis principal está en procesamiento de imagen médica, aprendizaje automático aplicado a datos biomédicos y procesamiento digital de señales.

> **EN —** Academic portfolio in computational biomedical engineering, with emphasis on medical image processing, biomedical machine learning, and biosignal analysis. Projects include multimodal PET–MRI registration, MRI classification with Grad-CAM, patient-level data leakage analysis, polysomnography signal analysis, analogue/digital filter design, numerical methods, and embedded systems. Documentation is primarily in Spanish, with English summaries in each project README.

---

## Trabajo técnico destacado

| Proyecto | Qué demuestra | Stack principal |
|---|---|---|
| **[Registro rígido multimodal PET–MRI](01-imagen-medica/registro-pet-mri/)** | Registro multimodal implementado de dos formas: transformación en GPU mediante shader GLSL + Información Mutua Normalizada + Powell, y una referencia con SimpleITK + Mattes MI | PyOpenGL, GLSL, SimpleITK, SciPy |
| **[Fuga de datos en ML médico](02-ia-diagnostico/fuga-datos-ml-medico/)** | Diferencia entre una partición aleatoria y una división por paciente; muestra cómo la fuga de información puede inflar el AUC y ocultar una mala generalización | scikit-learn, XGBoost, GroupShuffleSplit |
| **[CNN para Alzheimer + Grad-CAM](02-ia-diagnostico/cnn-alzheimer-gradcam/)** | CNN entrenada desde cero sobre MRI, evaluación con métricas estándar e interpretabilidad mediante Grad-CAM | TensorFlow/Keras, scikit-learn |
| **[Análisis espectral de apnea del sueño](03-senales-biomedicas/apnea-sueno-analisis-espectral/)** | Análisis de registros polisomnográficos reales de PhysioNet segmentados por evento respiratorio | SciPy, pandas, PhysioNet |
| **[Fusión wavelet PET–MRI](01-imagen-medica/fusion-wavelet-pet-mri/)** | Comparación de familias wavelet, niveles de descomposición y reglas de combinación para fusión multimodal | PyWavelets, OpenCV, PyOpenGL |
| **[ESP32 — Control de NeoPixel](05-sistemas-embebidos/esp32-control-neopixel/)** | Firmware basado en eventos con ADC, encoder rotatorio, antirrebote y máquina de estados | MicroPython, ESP32 |

---

## Áreas del portafolio

| | Área | Proyectos | Contenido |
|---|---|---:|---|
| 🧠 | **[Imagen médica](01-imagen-medica/)** | 5 | Registro multimodal PET–MRI, fusión wavelet, *reslicing* oblicuo, deformaciones geométricas, visualización volumétrica |
| 🤖 | **[IA biomédica y ML médico](02-ia-diagnostico/)** | 4 | CNN sobre MRI, ML clásico, fuga de datos por paciente y aprendizaje no supervisado |
| 📈 | **[Señales biomédicas](03-senales-biomedicas/)** | 8 | Apnea del sueño, ventriculografía, PPG por video, EEG, ECG y diseño de filtros |
| 🔢 | **[Métodos numéricos](04-metodos-numericos/)** | 4 | Integración numérica, descenso por gradiente, perceptrón, interpolación y mínimos cuadrados |
| ⚡ | **[Sistemas embebidos](05-sistemas-embebidos/)** | 2 | ESP32/MicroPython, control por eventos, periféricos e interacción física |

---

## Stack técnico

| Categoría | Herramientas |
|---|---|
| Lenguajes | Python, C, MicroPython, GLSL |
| Cómputo científico | NumPy, SciPy, SymPy, pandas |
| Machine learning | TensorFlow/Keras, scikit-learn, XGBoost, imbalanced-learn |
| Imagen médica | SimpleITK, PyWavelets, OpenCV, Pillow |
| Señales biomédicas | MNE, NeuroKit2, WFDB, PySpice |
| Gráficos / GPU | PyOpenGL, GLUT/GLFW, shaders GLSL |
| Visualización | Matplotlib, seaborn |
| Embebidos | ESP32, MicroPython, NeoPixel, encoders, ADC |

---

## Reproducibilidad y alcance

- **Los notebooks conservan sus salidas**, por lo que las gráficas, métricas y resultados pueden inspeccionarse directamente en GitHub.
- Varios notebooks fueron desarrollados en **Google Colab** y conservan sus rutas originales de Drive; cada README documenta el origen de los datos y las condiciones de ejecución.
- Los archivos pequeños necesarios para reproducir algunos proyectos se incluyen en el repositorio. Los datasets grandes o materiales sujetos a restricciones académicas no se redistribuyen.
- Cada área cuenta con su propio `requirements.txt` cuando corresponde.
- Los proyectos de clasificación o análisis biomédico aquí incluidos son **trabajos académicos y experimentales**. No constituyen herramientas clínicas validadas ni sistemas destinados a diagnóstico médico real.

---

## Contexto académico y autoría

Estos proyectos fueron desarrollados como prácticas, retos y trabajos de curso. Cuando una actividad partió de una plantilla, material de clase o conjunto de datos proporcionado por un profesor, se indica explícitamente en el README correspondiente.

| Curso | Institución | Material de partida |
|---|---|---|
| IA para el diagnóstico de enfermedades neurodegenerativas | Tecnológico de Monterrey | Plantillas de laboratorio del **Dr. Alejandro Santos Díaz** |
| Métodos Computacionales en Ingeniería Biomédica (MCIB) | UAM | Material de clase de **Raquel Valdés** |
| Machine Learning | UNAM | Material del curso |
| Visualización e Imagenología Médica por Computadora (VIMC) | UAM | Enunciados y pilas de imágenes del curso |
| Filtros Analógicos y Digitales (FAyD) | UAM | Enunciados de práctica |
| Procesamiento Digital de Señales Biomédicas | UAM | Enunciados de práctica |
| Señales y Medición (SyM) | UAM | Proyecto libre y proyecto final |

La implementación, adaptación, experimentación, resultados y análisis presentados en este repositorio son míos, salvo donde se indique expresamente lo contrario.

---

## Licencia

[MIT](LICENSE) — Rafael Uriostegui Sánchez
