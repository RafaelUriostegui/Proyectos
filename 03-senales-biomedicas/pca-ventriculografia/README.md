# PCA aplicado a ventriculografía radioisotópica (VRIE)

> **EN —** Principal Component Analysis applied to equilibrium radionuclide ventriculography studies.
> The method decomposes dynamic cardiac studies into their main spatial and temporal patterns,
> separating ventricular contraction from background activity and noise across eight patient studies.

## Contexto clínico

La **Ventriculografía Radioisotópica en Equilibrio (VRIE)** evalúa de forma no invasiva la función
ventricular. Tras marcar los eritrocitos del paciente con **Tecnecio-99m**, se adquiere una secuencia
de imágenes sincronizada con el ECG, obteniendo la evolución de la actividad a lo largo del ciclo
cardiaco.

## Objetivo

Extraer los principales **patrones espaciales y temporales** de la actividad ventricular mediante
Análisis de Componentes Principales, reduciendo una secuencia dinámica completa a unas pocas
componentes interpretables.

## Contenido

1. Carga de los ocho estudios (`N11`, `N12`, `N14`, `N23`, `P11`, `P12`, `P13`, `P14`).
2. Reorganización de cada estudio dinámico en matriz *píxeles × tiempo*.
3. Cálculo del ACP y análisis de varianza explicada por componente.
4. Interpretación de las primeras componentes: contracción ventricular, fondo y ruido.
5. Comparación entre estudios y exportación de resultados.

## Stack

`scikit-learn` (`PCA`) · `SciPy` (`loadmat`) · `NumPy` · `pandas` · `Matplotlib`

## Datos

[`datos/`](datos/) contiene los ocho estudios en formato `.mat` (~450 KB cada uno).

## Cómo ejecutar

```bash
pip install numpy scipy scikit-learn pandas matplotlib
jupyter notebook pca-ventriculografia.ipynb
```

---

<sub>Práctica 5 de Procesamiento Digital de Señales Biomédicas — Ingeniería Biomédica, UAM.</sub>
