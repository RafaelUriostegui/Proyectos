# Integración numérica aplicada a curvas de glucosa

> **EN —** Numerical integration worked out from first principles — trapezoidal rule and higher-order
> methods derived with their LaTeX formulation, error analysis and convergence behaviour — then
> applied to simulated glucose curves to compute area under the curve.

## Objetivo

Aproximar integrales definidas cuando no hay primitiva analítica, que es el caso habitual con datos
medidos. El notebook desarrolla la teoría y la aplica al cálculo del **área bajo la curva** de
respuestas de glucosa.

## Contenido

Un desarrollo largo (71 celdas) con la deducción matemática escrita en LaTeX:

1. **Regla del trapecio**: por qué mejora a la suma de Riemann, deducción de la fórmula y su versión
   compuesta.
2. Métodos de orden superior y comparación entre ellos.
3. **Análisis del error** de truncamiento y comportamiento de la convergencia al refinar la partición.
4. Contraste contra `scipy.integrate`.
5. **Aplicación**: área bajo la curva de dos simulaciones de glucosa.

## Stack

`SciPy` · `NumPy` · `Matplotlib` · `seaborn`

## Datos

[`datos/`](datos/) — `Glucosa_1_sim.mat` y `Glucosa_2_sim.mat`.

## Cómo ejecutar

```bash
pip install numpy scipy matplotlib seaborn
jupyter notebook integracion-numerica.ipynb
```

---

<sub>Práctica 4 de Métodos Computacionales en Ingeniería Biomédica (MCIB) — UAM, trimestre 26-P.</sub>
