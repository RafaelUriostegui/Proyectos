# IA para diagnóstico

> **EN —** Machine learning and deep learning applied to medical diagnosis, with an emphasis on
> methodological rigour: model interpretability with Grad-CAM and an explicit study of data leakage
> from patient-level splitting.

Aprendizaje automático y profundo aplicado a diagnóstico médico.

| Proyecto | Descripción | Stack |
|---|---|---|
| [CNN Alzheimer + Grad-CAM](cnn-alzheimer-gradcam/) | Red convolucional entrenada desde cero sobre MRI, con evaluación completa e interpretabilidad Grad-CAM | TensorFlow/Keras, scikit-learn |
| [Parkinson con ML clásico](parkinson-ml-clasico/) | Cinco algoritmos clásicos + XGBoost sobre biomarcadores acústicos de voz, con SMOTE | scikit-learn, XGBoost, imbalanced-learn |
| [Fuga de datos en ML médico](fuga-datos-ml-medico/) | AUC inflado por división aleatoria frente al desempeño real con división por paciente | scikit-learn, XGBoost |
| [Biomarcadores y no supervisado](biomarcadores-ml-unam/) | Parser `.skeleton` propio, biomarcadores de ejercicio, *clustering* y regresión; extracción de biomarcadores ECG | scikit-learn, NeuroKit2, WFDB |

## Instalación

```bash
pip install -r requirements.txt
```
