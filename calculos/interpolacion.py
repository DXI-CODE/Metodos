import numpy as np

def calcular_interpolacion(puntos):
    x_vals = np.array([p[0] for p in puntos])
    y_vals = np.array([p[1] for p in puntos])

    if len(set(x_vals)) != len(x_vals):
        raise ValueError('Los valores de X deben ser únicos.')

    vandermonde = np.vander(x_vals, increasing=True)
    coeficientes = np.linalg.solve(vandermonde, y_vals)

    terms = [f"{coef:.4f}*x**{i}" for i, coef in enumerate(coeficientes)]
    return " + ".join(terms)
