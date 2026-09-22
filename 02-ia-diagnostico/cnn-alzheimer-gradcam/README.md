# CNN para clasificación de Alzheimer + Grad-CAM

> **EN —** Academic convolutional neural network trained **from scratch** (no pretrained weights) in TensorFlow/Keras to classify Alzheimer's disease vs. healthy controls on a public MRI dataset, evaluated with standard classification metrics and interpreted with Grad-CAM heat maps.

## Objetivo

Explorar una tarea binaria de clasificación **Alzheimer (AD) vs. control sano (HC)** a partir de imágenes de resonancia magnética mediante una CNN entrenada desde pesos aleatorios. Se evita deliberadamente el *transfer learning* para observar el comportamiento de una arquitectura convolucional básica entrenada desde cero.

## Contenido

1. Carga y exploración del dataset público de MRI (`datasets` de Hugging Face).
2. Análisis de balance de clases y preprocesamiento de imágenes.
3. Arquitectura CNN construida capa por capa.
4. Entrenamiento con seguimiento de curvas de pérdida y exactitud.
5. Evaluación mediante matriz de confusión, precision, recall, F1 y curva ROC.
6. **Interpretabilidad con Grad-CAM** para visualizar qué regiones influyen en cada predicción.

## Stack

`TensorFlow` / `Keras` · `scikit-learn` · `NumPy` · `pandas` · `Matplotlib` · `seaborn` · `Pillow` · `datasets`

## Cómo ejecutar

Pensado para **Google Colab con GPU**. El dataset se descarga desde el notebook, por lo que no requiere archivos locales.

> El notebook conserva sus salidas: curvas de entrenamiento, métricas y mapas Grad-CAM pueden inspeccionarse directamente en GitHub sin ejecutarlo.

## Alcance

Este trabajo es **académico y experimental**. Las métricas obtenidas sobre este dataset no equivalen a validación clínica, y los mapas Grad-CAM deben interpretarse como una herramienta exploratoria de explicabilidad, no como evidencia causal ni biomarcadores validados.

---

<sub>Reto del curso «IA para el diagnóstico de enfermedades neurodegenerativas» (sesión 4) — Tecnológico de Monterrey, julio 2026. Plantilla del Dr. Alejandro Santos Díaz; desarrollo y resultados propios.</sub>
