# Filtro Butterworth analógico: diseño, simulación y construcción

> **EN —** End-to-end analogue filter project: designing a Butterworth filter from its specification,
> verifying it symbolically and numerically in Python, simulating the actual circuit with SPICE
> through PySpice, and finally building it physically and comparing measurements against the model.

## Por qué es interesante

Cubre el ciclo completo de un filtro analógico — de la especificación matemática al circuito armado —
y contrasta **tres niveles de modelado**: la función de transferencia ideal, la simulación SPICE con
componentes reales, y la medición del circuito construido.

## Contenido

1. **Especificación**: frecuencias de paso y rechazo, rizo permitido y atenuación requerida.
2. **Diseño**: cálculo del orden y de la función de transferencia Butterworth
   (`scipy.signal`, con verificación simbólica en `sympy`).
3. **Respuesta en frecuencia** teórica: magnitud, fase y diagrama de polos y ceros.
4. **Simulación SPICE** del circuito con `PySpice`, usando valores comerciales de componentes.
5. **Construcción física** y comparación de la respuesta medida contra la simulada.

## Stack

`PySpice` · `SciPy` · `SymPy` · `NumPy` · `Matplotlib`

## Cómo ejecutar

Pensado para **Google Colab**. `PySpice` requiere el motor **ngspice** instalado en el sistema.

> El notebook carga `ecg_noisy2.mat` desde Google Drive; ese archivo no está disponible localmente,
> pero las salidas guardadas muestran todos los resultados.

---

<sub>Práctica 1 de Filtros Analógicos y Digitales (FAyD) — UAM.</sub>
