# Biomarcadores y aprendizaje no supervisado

> **EN —** Two notebooks from a UNAM machine-learning course: extracting cardiac biomarkers from raw
> ECG with NeuroKit2/WFDB, and an unsupervised pipeline over motion-capture data that includes a
> hand-written `.skeleton` parser, exercise biomarkers, clustering and regression against performance
> scores.

## Los dos notebooks

### 1. [`biomarcadores-ecg.ipynb`](biomarcadores-ecg.ipynb)

Descarga un registro de ECG desde **PhysioNet** con `wfdb` y extrae biomarcadores cardiacos con
`neurokit2`: detección de complejos QRS, intervalos R-R y variabilidad de la frecuencia cardiaca.

### 2. [`clustering-biomarcadores-movimiento.ipynb`](clustering-biomarcadores-movimiento.ipynb)

Pipeline completo de aprendizaje **no supervisado** sobre datos de captura de movimiento:

- **Parser propio** del formato `.skeleton` (lectura de coordenadas articulares cuadro a cuadro).
- Cálculo de biomarcadores de ejercicio a partir de las trayectorias articulares.
- Procesamiento por lotes de todos los archivos del dataset.
- **Clustering** con selección del número de grupos por método del codo y coeficiente de silueta.
- Reducción de dimensionalidad con **PCA**.
- Cruce con las puntuaciones de desempeño de los participantes y **regresión**.
- Exportación de resultados a CSV.

## Stack

`scikit-learn` · `neurokit2` · `wfdb` · `pandas` · `NumPy` · `SciPy` · `Matplotlib` · `seaborn`

## Cómo ejecutar

Pensados para **Google Colab**; el notebook de ECG descarga sus datos de PhysioNet. El de movimiento
espera un `.zip` con los archivos `.skeleton` y el CSV
`Participants_with_Performance_Scores.csv`, material del curso que no se incluye aquí.

> Ambos notebooks conservan sus salidas, así que las gráficas de clustering y los biomarcadores
> calculados se ven directamente en GitHub.

---

<sub>Curso de Machine Learning — UNAM, 2026.</sub>
