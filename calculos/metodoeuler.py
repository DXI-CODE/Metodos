import numpy as np
import sympy as sp

def metodo_euler(valores):
    funcion = valores["funcion"]
    x0 = float(valores["x0"])
    xn = float(valores["xn"])
    y0 = float(valores["y0"])
    seleccion = valores["seleccion"]
    valor = float(valores["valor"])
    
    x, y = sp.symbols('x y')
    function = sp.lambdify([x, y], funcion, 'numpy')
    
    if seleccion == "n":
        n = int(valor)
        if n <= 0:
            raise ValueError("El número de pasos 'n' debe ser mayor que cero.")
        h = (xn - x0) / n
    elif seleccion == "h":
        h = valor
        if h <= 0:
            raise ValueError("El tamaño del paso 'h' debe ser mayor que cero.")
        n = int((xn - x0) / h)
        if n <= 0:
            raise ValueError("El tamaño del paso 'h' genera un número de pasos inválido.")
    else:
        raise ValueError("La selección debe ser 'n' o 'h'.")
    
    x_vals = [x0]
    y_vals = [y0]
    
    for i in range(n):
        x_next = x_vals[-1] + h
        y_next = y_vals[-1] + h * function(x_vals[-1], y_vals[-1])
        x_vals.append(x_next)
        y_vals.append(y_next)
    
    return {
        "numero": y_vals[-1],
        "n": n
    }