import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import sympy as sp

def metodo_trapecio(funcion_str, a, b, n):
    """
    Calcula la aproximación de la integral definida usando el método de trapecios.

    Args:
        funcion_str (str): La función a integrar (en términos de 'x').
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        n (int): Número de subintervalos.

    Returns:
        dict: Contiene 'resultado' (float) y 'grafico_base64' (str).
    """
    # Definir la variable simbólica
    x = sp.symbols('x')

    # Convertir el string a una expresión simbólica
    try:
        funcion = sp.sympify(funcion_str)
    except sp.SympifyError:
        raise ValueError("La función proporcionada no es válida")

    # Convertir la función simbólica a una función numérica
    f = sp.lambdify(x, funcion, 'numpy')

    # Calcular el valor de la integral por el método del trapecio
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        suma += 2 * f(a + i * h)
    integral = (h / 2) * suma

    # Generar la gráfica
    x_vals = np.linspace(a, b, 400)
    y_vals = f(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=f'Función: {funcion_str}', color='blue')

    # Agregar los trapecios
    for i in range(n):
        x0 = a + i * h
        x1 = x0 + h
        ax.fill_between([x0, x1], 0, [f(x0), f(x1)], color='orange', alpha=0.3)

    ax.axhline(0, color='black',linewidth=1)
    ax.axvline(0, color='black',linewidth=1)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.set_title(f'Integración por Trapecios (n={n})')

    # Convertir la gráfica a base64
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)

    return {'resultado': integral, 'grafico': grafico_base64}
