# Métodos numéricos

> **EN —** Numerical and optimisation methods implemented from first principles — integration,
> gradient descent, the perceptron, interpolation and least-squares fitting — each applied to real
> biomedical data rather than synthetic examples.

Métodos numéricos y de optimización implementados desde cero, aplicados a datos biomédicos.

| Proyecto | Descripción | Stack |
|---|---|---|
| [Integración numérica](integracion-numerica/) | Regla del trapecio y métodos de orden superior con deducción en LaTeX, análisis de error y área bajo curvas de glucosa | SciPy, NumPy |
| [Gradiente y perceptrón](gradiente-y-perceptron/) | Descenso por gradiente a mano con barrido de tasas, ajuste de pesos del perceptrón y evaluación de pruebas diagnósticas | scikit-learn, NumPy |
| [Interpolación y *morphing*](interpolacion-y-morphing/) | Splines cúbicos y de orden variable; efecto de la interpolación en redimensionamiento y *morphing* de imagen médica | SciPy, OpenCV |
| [Decaimiento radiactivo](decaimiento-radiactivo/) | Ajuste por mínimos cuadrados sobre modelo linealizado; separación de vida media física y biológica | SciPy, NumPy |

## Instalación

```bash
pip install -r requirements.txt
```
