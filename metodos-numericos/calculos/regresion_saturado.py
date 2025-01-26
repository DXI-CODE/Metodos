import numpy as np
from sympy import symbols, Eq, latex
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def graficar_comparativa(x_vals, y_reales, y_regresion):
    """
    Genera una gráfica comparativa entre valores reales y de regresión.

    Args:
        x_vals (list or numpy array): Valores del eje X.
        y_reales (list or numpy array): Valores reales en el eje Y.
        y_regresion (list or numpy array): Valores de regresión en el eje Y.
    """
    fig, ax = plt.subplots()

    # Graficar valores reales
    ax.scatter(x_vals, y_reales, color='blue', label='Valores reales', alpha=0.7)

    # Graficar valores de regresión
    ax.plot(x_vals, y_regresion, color='red', label='Valores de regresión', linestyle='--')

    # Etiquetas y título
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Comparativa: Valores Reales vs. Regresión')
    ax.legend()

    # Convertir la gráfica a formato base64 para usar en HTML
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')
    return graph_url

def metodo_regresion_crecimiento_saturado(datos_lin, datos):
    try:
        if not datos_lin or 'datos_lin_x' not in datos_lin or 'datos_lin_y' not in datos_lin:
            return {"error": "Los datos proporcionados no son válidos. Asegúrate de incluir 'x' y 'y'."}
        x_vals = datos_lin['datos_lin_x']
        y_vals = datos_lin['datos_lin_y']
        
        if not x_vals or not y_vals or len(x_vals) != len(y_vals):
            return {"error": "Las listas 'x' e 'y' deben tener datos y ser del mismo tamaño."}

        sumx = 0
        sumy = 0
        sumx2 = 0
        sumxy = 0
        for x_val, y_val in zip(x_vals, y_vals):
            if x_val == "Null" or y_val == "Null":
                return {"error": "'x' o 'y' tienen un valor Null, lo cual no es válido."}
            else:
                x_val = float(x_val)
                y_val = float(y_val)
                sumx += x_val
                sumy += y_val
                sumx2 += x_val * x_val
                sumxy += x_val * y_val

        matriz = np.zeros((2, 2))

        matriz[0][0] = len(x_vals)
        matriz[0][1] = sumx
        matriz[1][0] = sumx
        matriz[1][1] = sumx2
        matrizc = np.zeros((2, 1))
        matrizc[0][0] = sumy
        matrizc[1][0] = sumxy
        if np.linalg.det(matriz) == 0:
            return {"error": "La matriz no es invertible."}
        inversa = np.linalg.inv(matriz)
        mult = np.dot(inversa, matrizc)
        alpha = 1/mult[0][0]
        beta = mult[1][0] * alpha
        if beta == 0:
            return {"error": "El valor de beta es 0, lo cual no es válido para la fórmula."}
        ycal = []
        x_datos = datos['x']
        for x in x_datos:
            x = float(x)
            aux = (alpha * x) / (beta + x)
            ycal.append(aux)
        X, Y = symbols('X Y')
        expresion = Eq(Y, (alpha * X) / (beta + X))
        latex_ecuacion = latex(expresion)
        y_datos = datos['y']
        grafico_url = graficar_comparativa(x_datos, y_datos, ycal)
        return {
            "tabla_ycal" : ycal,
            "funcion" : latex_ecuacion,
            "tabla_x" : x_datos,
            "tabla_y" : y_datos,
            "grafico" : grafico_url
        }
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}