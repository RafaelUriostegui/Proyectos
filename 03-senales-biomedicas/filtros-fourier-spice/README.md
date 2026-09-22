# Espectros de Fourier, diseño de filtros y secciones de segundo orden

> **EN —** Analyses noisy ECG signals through their Fourier spectra, proposes filters from what the
> spectra reveal, implements the filtering, decomposes the result into cascaded second-order sections
> and validates each stage with SPICE simulation.

## Contenido

1. **Señales y espectros de Fourier**: análisis del contenido frecuencial de registros de ECG con
   ruido, para identificar qué hay que eliminar.
2. **Propuesta de filtros** justificada por lo observado en el espectro.
3. **Filtrado de señales** y comparación antes/después en tiempo y frecuencia.
4. **Secciones de segundo orden**: descomposición del filtro en etapas en cascada — la forma en que
   realmente se implementa un filtro de orden alto, por estabilidad numérica.
5. **Simulación SPICE** de cada sección de segundo orden con `PySpice`.
6. **Simulación del filtro final** completo.

## Stack

`PySpice` · `SciPy` · `NumPy` · `Matplotlib`

## Datos

[`datos/ecg_noisy.mat`](datos/) — registro de ECG con ruido, incluido en el repositorio.

> El notebook referencia además `ecg_noisy2.mat` desde Google Drive; ese archivo no está disponible
> localmente. Las salidas guardadas muestran los resultados de ambos.

## Cómo ejecutar

Pensado para **Google Colab**. `PySpice` requiere el motor **ngspice**.

---

<sub>Práctica 2 de Filtros Analógicos y Digitales (FAyD) — UAM.</sub>
