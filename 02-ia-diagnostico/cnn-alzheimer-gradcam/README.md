# CNN para clasificación de Alzheimer + Grad-CAM

> **EN —** A convolutional neural network trained **from scratch** (no pretrained weights) in
> TensorFlow/Keras to separate Alzheimer's disease from healthy controls on a public MRI dataset,
> evaluated rigorously and interpreted with Grad-CAM heat maps showing which regions drive each
> prediction.

## Objetivo

Distinguir **Alzheimer (AD) vs. control sano (HC)** a partir de imágenes de resonancia magnética,
entrenando una CNN «vanilla» desde pesos aleatorios — deliberadamente sin *transfer learning*, para
observar qué aprende una red convolucional por sí sola.

## Contenido

1. Carga y exploración del dataset público de MRI (`datasets` de Hugging Face).
2. Análisis de balance de clases y preprocesamiento de imágenes.
3. Arquitectura CNN construida capa por capa.
4. Entrenamiento con seguimiento de curvas de pérdida y exactitud.
5. Evaluación: matriz de confusión, precisión/recall/F1, curva ROC.
6. **Interpretabilidad con Grad-CAM**: mapas de calor que muestran en qué región de la MRI se apoya
   la red para cada predicción.

## Stack

`TensorFlow` / `Keras` · `scikit-learn` · `NumPy` · `pandas` · `Matplotlib` · `seaborn` · `Pillow` ·
`datasets`

## Cómo ejecutar

Pensado para **Google Colab con GPU**. El dataset se descarga desde el notebook, no requiere archivos
locales.

> El notebook conserva todas sus salidas: curvas de entrenamiento, métricas y mapas Grad-CAM se ven
> directamente en GitHub sin ejecutarlo.

---

<sub>Reto del curso «IA para el diagnóstico de enfermedades neurodegenerativas» (sesión 4) — Tecnológico de Monterrey, julio 2026. Plantilla del Dr. Alejandro Santos Díaz; desarrollo y resultados propios.</sub>
