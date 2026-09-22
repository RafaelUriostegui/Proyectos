# Fuga de datos en ML médico: *split* aleatorio vs. por paciente

> **EN —** Demonstrates data leakage in medical machine learning. When a dataset contains several
> recordings per patient, a random train/test split lets the model memorise per-patient signatures
> and reports an inflated AUC. Re-running the same pipeline with a patient-level (grouped) split
> reveals the real generalisation performance to unseen patients.

## Por qué importa

Es el error metodológico más común — y más costoso — en aprendizaje automático aplicado a medicina.
Un modelo con AUC de 0.95 que en realidad memorizó la voz de cada paciente **no sirve en clínica**,
porque los pacientes nuevos no están en el conjunto de entrenamiento.

## Contenido

1. Entrenamiento con **división aleatoria** → AUC inflado (*leaky*).
2. Entrenamiento con **división por paciente** (`GroupShuffleSplit`) → AUC real.
3. Cuantificación de la diferencia entre ambos y explicación de su origen.
4. Discusión escrita sobre:
   - qué modelo generaliza mejor a pacientes no vistos;
   - por qué el *split* por paciente es indispensable con medidas repetidas por sujeto;
   - otras dos fuentes de fuga de datos en ML médico;
   - qué validación adicional exigiría desplegar el modelo en una clínica.

## Stack

`scikit-learn` · `XGBoost` · `imbalanced-learn` · `pandas` · `NumPy` · `Matplotlib` · `seaborn`

## Cómo ejecutar

Pensado para **Google Colab**. El dataset se descarga desde el notebook.

---

<sub>Tarea 1 del curso «IA para el diagnóstico de enfermedades neurodegenerativas» — Tecnológico de Monterrey, julio 2026. Plantilla del Dr. Alejandro Santos Díaz; desarrollo, resultados y análisis propios.</sub>
