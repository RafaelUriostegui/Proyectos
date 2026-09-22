# Análisis de Componentes Principales aplicado a EEG

> **EN —** Two complementary notebooks on PCA: one implementing the decomposition step by step from
> the covariance matrix and checking it against scikit-learn, the other applying PCA to real
> multichannel EEG to identify and remove artefact components.

## Los dos notebooks

### 1. [`pca-paso-a-paso.ipynb`](pca-paso-a-paso.ipynb)

ACP implementado **desde cero** para entender qué hace por dentro:

- Simulación de casos con estructura de correlación conocida.
- Cálculo manual: centrado, matriz de covarianza, eigenvectores y eigenvalores, proyección.
- Contraste del resultado contra `sklearn.decomposition.PCA` para validar la implementación.

### 2. [`filtrado-eeg-pca.ipynb`](filtrado-eeg-pca.ipynb)

Aplicación a **datos reales de EEG multicanal**:

- Carga de un registro con `MNE`.
- Descomposición en componentes principales.
- Identificación de las componentes que concentran artefactos.
- **Filtrado** por reconstrucción sin esas componentes, y comparación con la señal original.

## Stack

`scikit-learn` · `MNE` · `NumPy` · `Matplotlib`

## Cómo ejecutar

```bash
pip install numpy scikit-learn matplotlib mne
jupyter notebook pca-paso-a-paso.ipynb
```

> `filtrado-eeg-pca.ipynb` usa el registro `S001R01.edf` de la
> [EEG Motor Movement/Imagery Database](https://physionet.org/content/eegmmidb/) de PhysioNet, que no
> se incluye por tamaño; `MNE` puede descargarlo automáticamente.

---

<sub>Procesamiento Digital de Señales Biomédicas — UAM.</sub>
