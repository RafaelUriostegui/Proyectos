# IA biomédica y machine learning médico

> **EN —** Academic machine learning and deep learning projects applied to biomedical data, with emphasis on methodological rigor, patient-level validation, model interpretability, and limitations of experimental results.

Proyectos de aprendizaje automático y profundo aplicados a datos biomédicos. El foco no está en presentar herramientas clínicas terminadas, sino en documentar pipelines experimentales, evaluación, interpretabilidad y problemas metodológicos relevantes en ML médico.

| Proyecto | Descripción | Stack |
|---|---|---|
| [CNN Alzheimer + Grad-CAM](cnn-alzheimer-gradcam/) | CNN entrenada desde cero sobre MRI para clasificación binaria académica, con métricas estándar e interpretabilidad Grad-CAM | TensorFlow/Keras, scikit-learn |
| [Parkinson con ML clásico](parkinson-ml-clasico/) | Comparación de algoritmos clásicos y XGBoost sobre biomarcadores acústicos de voz, incluyendo tratamiento de desbalance | scikit-learn, XGBoost, imbalanced-learn |
| [Fuga de datos en ML médico](fuga-datos-ml-medico/) | Comparación entre split aleatorio y split por paciente para mostrar cómo la fuga de información puede inflar el AUC | scikit-learn, XGBoost |
| [Biomarcadores y no supervisado](biomarcadores-ml-unam/) | Extracción y análisis de biomarcadores, clustering y regresión sobre datos de ejercicio y ECG | scikit-learn, NeuroKit2, WFDB |

> **Alcance:** estos proyectos son ejercicios académicos y experimentales. Sus resultados no constituyen validación clínica ni deben interpretarse como desempeño diagnóstico en condiciones reales.

## Instalación

```bash
pip install -r requirements.txt
```
