# Decaimiento radiactivo y vida media biológica

> **EN —** Fits radioactive decay data by least squares. The exponential model is linearised to solve
> it in closed form, the decay constant and half-life are recovered, and the physical half-life is
> then separated from the biological one — the distinction that matters when a radiotracer is inside
> a patient.

## Modelo

$$\frac{dN}{dt} = -\lambda N$$

donde `N` es el número de átomos en el tiempo, `dN/dt` la tasa de desintegración por unidad de tiempo
y `λ` la constante de desintegración.

## Contenido

1. Planteamiento de la ecuación diferencial y su solución analítica.
2. **Solo decaimiento físico**: ajuste sobre los datos medidos.
3. **Mínimos cuadrados** aplicados tras **linealizar** los datos (log del modelo exponencial), lo que
   convierte el ajuste no lineal en una regresión lineal resoluble en forma cerrada.
4. **Vida media biológica**: separación de la componente de eliminación fisiológica respecto de la
   desintegración física — la vida media efectiva no es ninguna de las dos por separado.
5. **Error de ajuste** y evaluación de la calidad del modelo.

## Stack

`SciPy` · `NumPy` · `Matplotlib`

## Datos

[`datos/Datos3.mat`](datos/) — mediciones de actividad.

## Cómo ejecutar

```bash
pip install numpy scipy matplotlib
jupyter notebook decaimiento-radiactivo.ipynb
```

---

<sub>Práctica 2 de Métodos Computacionales en Ingeniería Biomédica (MCIB) — UAM.</sub>
