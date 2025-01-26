import numpy as np
import sympy as sp
import math as math

def exponencial(puntos):
    x_vals = np.array([p[0] for p in puntos])
    y_vals = np.array([math.log(p[1]) for p in puntos])
    x2_vals = np.array([p**2 for p in x_vals], dtype=float)
    xy_vals = np.array([x * y for x, y in zip(x_vals, y_vals)])

    mat1 = np.array([[len(x_vals), np.sum(x_vals)], [np.sum(x_vals), np.sum(x2_vals)]], dtype=float)
    mat2 = np.array([np.sum(y_vals), np.sum(xy_vals)], dtype=float)

    matinv = np.linalg.inv(mat1)  
    final = np.dot(matinv, mat2) 
    
    x = sp.symbols('x')
    a, b = final  
    expr = math.exp(a) * sp.exp(b * x)  
    
    return sp.latex(expr)
 