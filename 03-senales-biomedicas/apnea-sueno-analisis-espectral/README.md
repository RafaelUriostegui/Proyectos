# Análisis espectral de apnea del sueño

> **EN —** A full hypothesis-driven study of respiratory events in polysomnography record `slp59m`
> from PhysioNet's Sleep Database. Respiratory signals are segmented by annotated event type
> (obstructive apnea, central apnea, hypopnea, arousal) and compared against event-free windows
> through spectrograms and spectral power distribution.

## Hipótesis de trabajo

> Durante los episodios de apnea o hipopnea se producen cambios identificables en las señales
> respiratorias y en su contenido espectral, acompañados de alteraciones en el ECG y la presión
> arterial.

El documento `ApneaSueño.pdf` del curso se usó como marco de referencia para interpretar los eventos.
Aunque está dirigido a población pediátrica, sus definiciones de apnea obstructiva, apnea central e
hipopnea coinciden con el código de marcas de `slpdb` y sirven como **criterio de interpretación, no
como diagnóstico**, para este registro adulto.

## Contenido

1. Lectura del registro `slp59m` (7 señales, 900 000 muestras, 250 Hz, 1 hora de duración).
2. Parseo del archivo de marcas para localizar cada evento respiratorio anotado.
3. Segmentación de ventanas por tipo de evento:
   - apnea obstructiva (`X`)
   - apnea central (`CAA`)
   - hipopnea (`H`)
   - *arousal* (`HA`)
   - ventana de control sin evento
4. **Espectrogramas** de cada tipo de episodio y comparación conjunta alineada.
5. Análisis de distribución de potencia espectral por banda.

## Stack

`SciPy` (`spectrogram`, `welch`) · `NumPy` · `pandas` · `Matplotlib`

## Datos

[`datos/slp59m.mat`](datos/) — registro extraído de la
[MIT-BIH Polysomnographic Database (slpdb)](https://physionet.org/content/slpdb/) de PhysioNet,
incluido para que el notebook sea reproducible. El archivo de marcas
`MarcasRegistroslp59m.txt` procede de la misma fuente.

## Cómo ejecutar

```bash
pip install numpy scipy pandas matplotlib
jupyter notebook analisis-espectral-apnea.ipynb
```

---

<sub>Práctica 6 de Procesamiento Digital de Señales Biomédicas — UAM.</sub>
