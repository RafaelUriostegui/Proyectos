# Decodificación DTMF por análisis espectral

> **EN —** Recovers which keys were pressed on a telephone keypad from the audio alone. DTMF encodes
> each key as the sum of two sine tones — one from a low group, one from a high group — so the FFT of
> the signal reveals the exact pair, and the pair identifies the key.

## Cómo funciona DTMF

Cada tecla de un teclado telefónico emite **dos tonos simultáneos**: uno del grupo de frecuencias
bajas (697, 770, 852, 941 Hz) y uno del grupo alto (1209, 1336, 1477 Hz). La intersección de fila y
columna identifica la tecla de forma unívoca.

## Resultado del análisis

Las frecuencias detectadas en el espectro fueron **770, 852, 1209, 1336 y 1477 Hz**, lo que acota los
dígitos pulsados a: **4, 5, 6, 7, 8, 9**.

## Contenido

1. Carga de la señal de audio y visualización en el dominio del tiempo.
2. **FFT** y localización de los picos espectrales.
3. Identificación de los pares de frecuencias presentes.
4. Mapeo de cada par a su tecla correspondiente según la tabla DTMF.

## Stack

`SciPy` · `NumPy` · `Matplotlib` · `IPython.display` (reproducción de audio)

## Cómo ejecutar

Pensado para **Google Colab**; carga `Ref.png` (la tabla de frecuencias DTMF) desde Google Drive.
Ese archivo no está disponible localmente, pero el notebook conserva sus salidas y la imagen de
referencia queda incrustada en las celdas markdown.

---

<sub>Práctica 4 de Filtros Analógicos y Digitales (FAyD) — UAM.</sub>
