import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import math

def calcular_y_graficar(funcion_str, x0, tolerancia, iteraciones):
    try:
        x = sp.symbols('x')
        g = sp.sympify(funcion_str)
        valores_x = [x0]
        for _ in range(iteraciones):
            x_next = float(g.subs(x, valores_x[-1]))
            valores_x.append(x_next)
            if abs(valores_x[-1] - valores_x[-2]) < tolerancia:
                break

        raiz = valores_x[-1]

        x_vals = np.linspace(raiz - 2, raiz + 2, 500)
        g_func = sp.lambdify(x, g, 'numpy')
        y_vals = g_func(x_vals)

        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, label=f"g(x) = {funcion_str}", color="blue")
        plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
        plt.scatter([raiz], [g_func(raiz)], color="red", label=f"Raíz: x ≈ {raiz:.5f}")
        plt.title("Método de Punto Fijo")
        plt.xlabel("x")
        plt.ylabel("g(x)")
        plt.legend()
        plt.grid(True)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return buffer
    except Exception as e:
        raise ValueError(f"Error en el cálculo o graficación: {e}")
    
def metodo_punto_fijo_calculo(funcion_str, x0, tolerancia, iteraciones_max):

    context = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'sqrt': math.sqrt,
        'pi': math.pi
    }

    def g(x):
        return eval(funcion_str, {"x": x}, context) 

    iteracion = 0
    error = float('inf')
    x = x0

    while iteracion < iteraciones_max and error > tolerancia:
        x_next = g(x)
        error = abs(x_next - x)
        x = x_next
        iteracion += 1

    return x, error