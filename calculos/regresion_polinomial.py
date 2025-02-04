import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def regresion_polinomial(x_values, y_values, grado):
    """
    Realiza la regresión polinomial y genera una gráfica junto con la ecuación en formato LaTeX.

    Args:
        x_values (list or np.array): Valores de x.
        y_values (list or np.array): Valores de y.
        grado (int): Grado del polinomio.

    Returns:
        dict: Contiene 'polinomio_latex' (str) y 'grafico_base64' (str).
    """
    if len(x_values) != len(y_values):
        raise ValueError("Los valores de x e y deben tener la misma longitud.")
    if grado < 1:
        raise ValueError("El grado del polinomio debe ser al menos 1.")

    # Ajuste polinomial
    coeficientes = np.polyfit(x_values, y_values, grado)
    polinomio = np.poly1d(coeficientes)

    # Crear una expresión simbólica para el polinomio
    x = sp.symbols('x')
    polinomio_simbolico = sum(round(coef, 3) * x**i for i, coef in enumerate(reversed(coeficientes)))

    # Convertir el polinomio a LaTeX usando sympy
    polinomio_latex = sp.latex(polinomio_simbolico)

    # Generar gráfica
    x_min, x_max = min(x_values), max(x_values)
    x_grafico = np.linspace(x_min - 1, x_max + 1, 500)
    y_grafico = polinomio(x_grafico)

    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values, color='blue', label='Datos', zorder=5)
    ax.plot(x_grafico, y_grafico, color='red', label=f'Polinomio grado {grado}', zorder=4)
    ax.axhline(0, color='black', linewidth=1, linestyle='--', zorder=1)
    ax.axvline(0, color='black', linewidth=1, linestyle='--', zorder=1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.set_title('Regresión Polinomial')

    # Convertir gráfica a base64
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)

    return {'resultado': polinomio_latex, 'grafico': grafico_base64}
