# Detección de Parkinson con ML clásico

> **EN —** Detects Parkinson's disease from acoustic voice features, training and rigorously comparing
> five classical machine-learning algorithms plus XGBoost, with SMOTE to handle class imbalance.

## Objetivo

Clasificar pacientes con **enfermedad de Parkinson** frente a controles usando únicamente
**biomarcadores acústicos de voz** (jitter, shimmer, relación armónico-ruido, etc.), y comparar de
forma justa varios algoritmos clásicos.

## Contenido

1. Carga del dataset de voz y análisis exploratorio.
2. Escalamiento de características y tratamiento del **desbalance de clases con SMOTE**.
3. Entrenamiento de cinco algoritmos clásicos + **XGBoost**.
4. Comparación rigurosa: validación cruzada, matrices de confusión, AUC-ROC por modelo.
5. Análisis de importancia de características.

## Stack

`scikit-learn` · `XGBoost` · `imbalanced-learn` (SMOTE) · `pandas` · `NumPy` · `Matplotlib` · `seaborn`

## Cómo ejecutar

Pensado para **Google Colab**. El dataset se descarga desde el propio notebook (`urllib`), no
requiere archivos locales.

## Nota metodológica

Este notebook usa división aleatoria del dataset. El problema que eso introduce cuando hay varias
grabaciones por paciente se analiza a fondo en
[fuga-datos-ml-medico](../fuga-datos-ml-medico/) — conviene leerlos en ese orden.

---

<sub>Laboratorio 1 del curso «IA para el diagnóstico de enfermedades neurodegenerativas» (sesión 2) — Tecnológico de Monterrey, julio 2026. Plantilla del Dr. Alejandro Santos Díaz; desarrollo y resultados propios.</sub>
