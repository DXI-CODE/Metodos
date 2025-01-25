import numpy as np

def lagrange(puntos, grado, x):
    
    if(grado < 1 or grado > 4):
        raise ValueError('Elige un grado entre 1 y 4.')

    x_vals = np.array([p[0] for p in puntos])
    y_vals = np.array([p[1] for p in puntos])

    if len(set(x_vals)) != len(x_vals):
        raise ValueError('Los valores de X deben ser únicos.')
    
    if grado >= len(x_vals):
        raise ValueError(f'Debe haber al menos {grado + 1} valores para la interpolación.')
    
    sum = 0
    for i in range(grado + 1):
        product = y_vals[i]
        for j in range(grado + 1):
            if i != j:
                product *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])
        sum += product

    return sum