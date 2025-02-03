import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO
import base64
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
    f_expr = sp.lambdify(x, expr, 'numpy')
    y2 = [f_expr(fila[0]) for fila in puntos]

    y_valsog = np.array([fila[1] for fila in puntos])
    y_mean = np.mean(y_valsog )  
    ss_total = np.sum((y_valsog  - y_mean) ** 2)  
    ss_residual = np.sum((y_valsog - y2) ** 2)  
    r2 = 1 - (ss_residual / ss_total)  
    
    puntos_ord = sorted(puntos)
    
    try:
        fig, ax = plt.subplots()
        ax.plot([fila[0] for fila in puntos_ord], [fila[1] for fila in puntos_ord], label="Puntos originales")
        ax.plot([fila[0] for fila in puntos_ord], sorted(y2), label=f'f(x) = {str(expr)}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.set_title('Ecuación obtenida')

        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        grafico_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close(fig)
        print("Gráfica generada correctamente.")
    except Exception as e:
        print(f"Error al generar la gráfica: {e}")
        grafico_base64 = None
        return {'error': e}

    return {'grafico_base64': grafico_base64, 'r2': r2}
 