# Señales biomédicas

> **EN —** Biomedical digital signal processing: spectral analysis of polysomnography, PCA on
> radionuclide ventriculography, video-based photoplethysmography, and analogue/digital filter design
> validated end to end with SPICE simulation.

Procesamiento digital de señales biomédicas: EEG, ECG, respiración, PPG y diseño de filtros.

| Proyecto | Descripción | Stack |
|---|---|---|
| [Apnea del sueño](apnea-sueno-analisis-espectral/) | Espectrogramas por tipo de evento respiratorio sobre el registro `slp59m` de PhysioNet | SciPy, pandas |
| [ACP en ventriculografía](pca-ventriculografia/) | Patrones espacio-temporales de función ventricular en 8 estudios de cardiología nuclear | scikit-learn, SciPy |
| [PPG por video](ppg-por-video/) | Frecuencia cardiaca extraída de un video convencional mediante FFT y detección de picos | OpenCV, SciPy |
| [Filtro Butterworth + SPICE](filtro-butterworth-spice/) | Diseño → simulación SPICE → construcción física, con comparación de las tres | PySpice, SciPy, SymPy |
| [Fourier, filtros y SPICE](filtros-fourier-spice/) | Espectros de ECG con ruido, diseño de filtros y secciones de segundo orden en cascada | PySpice, SciPy |
| [Ondas alfa en EEG](filtrado-eeg-alfa/) | Aislamiento del ritmo alfa con Chebyshev I, justificando la elección del tipo de filtro | SciPy |
| [Decodificación DTMF](decodificacion-dtmf/) | Identificación de teclas pulsadas por los pares de frecuencias en el espectro | SciPy, NumPy |
| [ACP en EEG](filtrado-eeg-pca/) | ACP implementado desde cero y validado contra scikit-learn; remoción de artefactos en EEG real | scikit-learn, MNE |

## Instalación

```bash
pip install -r requirements.txt
```
