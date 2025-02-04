import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.optimize import curve_fit

# Definir el modelo exponencial
def modelo_exponencial(x, a0, a1):
    return a0 * (1 - np.exp(-a1 * x))

def regresion_no_lineal(x_vals, y_vals):
    """Realiza la regresión no lineal y devuelve los parámetros optimizados, R^2 y la gráfica."""
    x = np.array(x_vals, dtype=float)
    y = np.array(y_vals, dtype=float)

    # Ajustar el modelo a los datos
    parametros_optimizados, _ = curve_fit(modelo_exponencial, x, y)
    a0_opt, a1_opt = parametros_optimizados

    # Calcular los valores predichos
    y_predicho = modelo_exponencial(x, a0_opt, a1_opt)

    # Calcular el coeficiente de determinación R^2
    ss_res = np.sum((y - y_predicho) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_cuadrado = 1 - (ss_res / ss_tot)

    # Generar la gráfica
    img = io.BytesIO()
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, label='Datos observados')
    plt.plot(x, y_predicho, label='Modelo ajustado', color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.title('Regresión No Lineal: Modelo Exponencial')
    plt.grid()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    grafica_base64 = base64.b64encode(img.getvalue()).decode()

    # Devolver resultados
    return {
        'a0': round(a0_opt, 4),
        'a1': round(a1_opt, 4),
        'r2': round(r_cuadrado, 4),
        'grafica': grafica_base64
    }
