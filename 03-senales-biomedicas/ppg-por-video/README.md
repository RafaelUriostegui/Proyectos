# Fotopletismografía (PPG) a partir de video

> **EN —** Extracts a photoplethysmographic signal — and from it a heart rate — out of an ordinary
> video recording. Each frame is reduced to its mean saturation in the red channel, producing a time
> series sampled at the video's frame rate; the pulse frequency is then recovered by FFT and peak
> detection.

## Idea

Un video es, para estos efectos, una señal muestreada: **cada cuadro es una muestra** y los **cuadros
por segundo son la frecuencia de muestreo**. Si se graba tejido perfundido, la variación de color
entre cuadros sigue el pulso sanguíneo — el mismo principio de un pulsioxímetro, pero con una cámara
convencional.

## Método

1. Abrir el video con OpenCV y leer sus metadatos: número de cuadros (`N`) y `fps`.
2. Por cada cuadro, convertir a HSV y promediar la **saturación en el canal rojo** → una muestra.
3. Construir la señal PPG completa a partir de esos promedios.
4. Aplicar **FFT** para localizar la frecuencia dominante dentro del rango fisiológico.
5. Detección de picos (`scipy.signal.find_peaks`) para contar latidos y estimar la frecuencia
   cardiaca en latidos por minuto.

El registro analizado corresponde a una prueba de **100 LPM**.

## Stack

`OpenCV` · `NumPy` · `SciPy` (`fft`, `find_peaks`) · `Matplotlib`

## Cómo ejecutar

Pensado para **Google Colab**: el notebook monta Google Drive y lee el video desde
`MyDrive/PPG_videos/v10-100LPM.avi`. El video es material del curso y no se incluye aquí; para
ejecutarlo con otro archivo basta cambiar la ruta en la segunda celda.

> El notebook conserva sus salidas, así que la señal PPG reconstruida y el espectro se ven
> directamente en GitHub.

---

<sub>Procesamiento Digital de Señales Biomédicas — UAM.</sub>
