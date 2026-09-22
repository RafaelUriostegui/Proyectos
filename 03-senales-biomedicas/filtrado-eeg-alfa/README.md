# Filtrado de ondas alfa en EEG

> **EN —** Isolates alpha rhythm (8–13 Hz) from a real EEG recording. The notebook argues *why*
> Chebyshev type I is the right choice here — its sharper transition makes the alpha bursts visually
> distinct — then carries the design through to a digital implementation.

## Contexto

Las **ondas alfa** aparecen con los ojos cerrados y se manifiestan como «paquetes» rítmicos en el
EEG. Aislarlas exige un filtro con transición suficientemente abrupta para separarlas de las bandas
theta y beta adyacentes.

## Contenido

1. Análisis del EEG crudo y de su espectro.
2. **Justificación del tipo de filtro**: se elige **Chebyshev I** porque hace más visibles los
   paquetes de ondas alfa; se discute Chebyshev II como alternativa para el desarrollo digital.
3. Diseño del filtro analógico y su respuesta en frecuencia.
4. **Implementación digital** del filtro y aplicación a la señal.
5. Comparación de la señal antes y después del filtrado, en tiempo y frecuencia.

## Stack

`SciPy` (`signal`) · `NumPy` · `Matplotlib`

## Datos

[`datos/eeg.mat`](datos/) — registro de EEG incluido en el repositorio.

## Cómo ejecutar

```bash
pip install numpy scipy matplotlib
jupyter notebook filtrado-eeg-ondas-alfa.ipynb
```

> El notebook fue escrito en Colab y carga el `.mat` desde Google Drive; para ejecutarlo localmente
> apunta la ruta a `datos/eeg.mat`.

---

<sub>Práctica 3 de Filtros Analógicos y Digitales (FAyD) — UAM.</sub>
