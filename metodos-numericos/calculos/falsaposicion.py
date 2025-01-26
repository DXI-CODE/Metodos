import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def calcular_falsa_posicion(funcion_str, a, b, tolerancia, iteraciones):
    # Definir la variable simbólica
    x = sp.symbols('x')

    # Convertir el string a una expresión simbólica
    try:
        funcion = sp.sympify(funcion_str)
    except sp.SympifyError:
        raise ValueError("La función proporcionada no es válida")

    # Convertir la función simbólica a una función numérica
    f = sp.lambdify(x, funcion, 'numpy')

    # Inicializamos variables
    error = tolerancia + 1  # Inicializamos el error mayor que la tolerancia
    iteracion = 0
    prev_c = None
    c = None  # Para almacenar la raíz final

    while iteracion < iteraciones and error > tolerancia:
        # Calculamos el valor de f(a) y f(b)
        fa = f(a)
        fb = f(b)

        # Calculamos la nueva aproximación c
        c = b - (fb * (b - a)) / (fb - fa)
        fc = f(c)

        if np.isnan(fc) or np.isinf(fc):
            raise ValueError(f"Error en la iteración {iteracion}: Valor de fc indefinido")

        # Calculamos el error relativo
        if prev_c is not None:
            error = abs((c - prev_c) / c)
        prev_c = c

        # Actualizamos los valores de a y b
        if fa * fc < 0:
            b = c
        else:
            a = c

        iteracion += 1

    # Generar la gráfica
    x_vals = np.linspace(a - 2, b + 2, 400)
    y_vals = f(x_vals)

    fig, ax = plt.subplots()

    # Graficar la función
    ax.plot(x_vals, y_vals, label=f'Función: {funcion_str}', color='blue')

    # Marcar el punto raíz encontrado
    ax.plot(c, 0, 'ro', label=f'Raíz: x = {c:.6f}')

    # Líneas de referencia
    ax.axhline(0, color='black', linewidth=1, linestyle='--')
    ax.axvline(0, color='black', linewidth=1, linestyle='--')

    # Etiquetas y título
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Método de Falsa Posición')
    ax.legend()

    # Convertir la gráfica a formato base64 para usar en HTML
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return {'raiz': c, 'graph_url': graph_url}
