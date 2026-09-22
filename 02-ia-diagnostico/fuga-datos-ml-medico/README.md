# Fuga de datos en ML médico: *split* aleatorio vs. por paciente

> **EN —** Demonstrates data leakage in medical machine learning. When a dataset contains several recordings per patient, a random train/test split can let the model exploit patient-specific signatures and report an inflated AUC. Re-running the same pipeline with a patient-level grouped split provides a more realistic estimate of generalisation to unseen patients.

## Por qué importa

Cuando existen múltiples registros por paciente, dividir las muestras aleatoriamente puede colocar datos del mismo sujeto tanto en entrenamiento como en prueba. El modelo puede entonces aprovechar características propias del paciente en lugar de aprender patrones que generalicen a sujetos nuevos.

Un AUC alto bajo ese esquema **no demuestra generalización clínica ni desempeño real sobre pacientes no vistos**.

## Contenido

1. Entrenamiento con **división aleatoria** → estimación potencialmente inflada por fuga de información.
2. Entrenamiento con **división por paciente** (`GroupShuffleSplit`) → evaluación sobre sujetos no vistos.
3. Cuantificación de la diferencia entre ambos esquemas y análisis de su origen.
4. Discusión sobre:
   - qué modelo generaliza mejor a pacientes no vistos;
   - por qué el *split* por paciente es necesario con medidas repetidas por sujeto;
   - otras fuentes de fuga de datos en ML médico;
   - qué validaciones adicionales serían necesarias antes de considerar un uso clínico.

## Stack

`scikit-learn` · `XGBoost` · `imbalanced-learn` · `pandas` · `NumPy` · `Matplotlib` · `seaborn`

## Cómo ejecutar

Pensado para **Google Colab**. El dataset se descarga desde el notebook.

---

<sub>Tarea 1 del curso «IA para el diagnóstico de enfermedades neurodegenerativas» — Tecnológico de Monterrey, julio 2026. Plantilla del Dr. Alejandro Santos Díaz; desarrollo, resultados y análisis propios.</sub>
