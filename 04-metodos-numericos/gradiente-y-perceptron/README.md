# Descenso por gradiente, perceptrón y pruebas diagnósticas

> **EN —** Three notebooks covering optimisation and linear classification from the ground up:
> gradient descent implemented by hand with a learning-rate sweep, perceptron weight fitting, and
> both applied to real bivariate clinical data (glucose and glycated haemoglobin) for diagnostic
> test evaluation.

## Los tres notebooks

### 1. [`gradiente-perceptron-glucosa.ipynb`](gradiente-perceptron-glucosa.ipynb)

- **Descenso por gradiente** sobre `J(u) = 2(u−1)² + 1`, implementado a mano, partiendo de `u₀ = 4`
  y comparando tasas de aprendizaje **ρ = 0.5, 0.25, 0.1**. Muestra cómo la tasa determina si el
  algoritmo converge, oscila o diverge.
- **Ajuste del vector de pesos de un perceptrón** para clasificar datos etiquetados.
- **Datos bivariados reales**: glucosa vs. hemoglobina glucosilada (HbA1c).

### 2. [`evaluacion-pruebas-diagnosticas.ipynb`](evaluacion-pruebas-diagnosticas.ipynb)

Aplica lo anterior a la **evaluación de pruebas diagnósticas de laboratorio**: separación de clases
sobre los datos de glucosa/HbA1c y análisis del desempeño del clasificador resultante.

### 3. [`ensayo-perceptron.ipynb`](ensayo-perceptron.ipynb)

Ensayo enfocado en el perceptrón: generación de datos, separación en entrenamiento y prueba,
entrenamiento, y visualización de la **recta de clasificación** sobre ambos conjuntos.

## Stack

`scikit-learn` · `SciPy` · `NumPy` · `Matplotlib`

## Datos

[`datos/`](datos/) — `DatosBivariados.mat` y sus particiones de entrenamiento y prueba.

## Cómo ejecutar

```bash
pip install numpy scipy scikit-learn matplotlib
jupyter notebook gradiente-perceptron-glucosa.ipynb
```

---

<sub>Métodos Computacionales en Ingeniería Biomédica (MCIB) — UAM, trimestre 26-P. Material de clase de Raquel Valdés; desarrollo y resultados propios.</sub>
