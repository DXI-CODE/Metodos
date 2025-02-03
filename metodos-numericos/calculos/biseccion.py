import math
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def f(c, g, m, t, v):
    """Función para la cual se calcula la raíz."""
    return (g * m / c) * (1 - math.exp(-c * t / m)) - v

def biseccion(f, xl, xu, tol, max_iter, g, m, t, v):
    """Método de Bisección con generación de gráficas."""
    iteraciones = 0
    xr = (xl + xu) / 2.0
    resultados = []
    x_values = []  # Almacenar valores de xr para graficar la convergencia

    while abs(f(xr, g, m, t, v)) > tol and iteraciones < max_iter:
        xr = (xl + xu) / 2.0
        resultado = {
            'iteracion': iteraciones + 1,
            'xl': xl,
            'xu': xu,
            'xr': xr,
            'f_xl': f(xl, g, m, t, v),
            'f_xu': f(xu, g, m, t, v),
            'f_xr': f(xr, g, m, t, v)
        }
        resultados.append(resultado)
        x_values.append(xr)

        if f(xl, g, m, t, v) * f(xr, g, m, t, v) < 0:
            xu = xr
        else:
            xl = xr
        
        iteraciones += 1

    # Generar las gráficas
    grafica_convergencia = generar_grafica_convergencia(x_values)
    grafica_funcion = generar_grafica_funcion(f, xl, xu, g, m, t, v, xr)

    return {
        'raiz': xr,
        'iteraciones': iteraciones,
        'resultados': resultados,
        'grafica_convergencia': grafica_convergencia,
        'grafica_funcion': grafica_funcion
    }

def generar_grafica_convergencia(x_values):
    """Genera la gráfica de convergencia del método de Bisección."""
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(x_values) + 1), x_values, marker='o', linestyle='-', color='b')
    plt.xlabel('Iteración')
    plt.ylabel('Valor de xr')
    plt.title('Convergencia del Método de Bisección')
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.getvalue()).decode()

def generar_grafica_funcion(f, xl, xu, g, m, t, v, raiz):
    """Genera la gráfica de la función con la raíz encontrada."""
    x_vals = np.linspace(xl, xu, 100)
    y_vals = [f(x, g, m, t, v) for x in x_vals]

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label='f(x)', color='blue')
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(raiz, color='red', linestyle='--', label=f'Raíz ≈ {raiz:.6f}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Gráfica de la Función y la Raíz')
    plt.legend()
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.getvalue()).decode()

