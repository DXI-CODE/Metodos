import numpy as np
import matplotlib.pyplot as plt
import base64
import io


# Función para calcular regresión por matrices
def regresion_por_matrices(tipo, x, y):
    x = np.array(x)
    y = np.array(y)
    
    if tipo == 'lineal':
        A = np.vstack([np.ones_like(x), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        y_cal = A @ coef
        equation = f"y = {coef[0]:.4f} + {coef[1]:.4f}x"
    
    elif tipo == 'cuadratica':
        A = np.vstack([np.ones_like(x), x, x**2]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        y_cal = A @ coef
        equation = f"y = {coef[0]:.4f} + {coef[1]:.4f}x + {coef[2]:.4f}x²"
    
    elif tipo == 'cubica':
        A = np.vstack([np.ones_like(x), x, x**2, x**3]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        y_cal = A @ coef
        equation = f"y = {coef[0]:.4f} + {coef[1]:.4f}x + {coef[2]:.4f}x² + {coef[3]:.4f}x³"

    # Calcular R²
    st = np.sum((y - np.mean(y))**2)
    sr = np.sum((y - y_cal)**2)
    r2 = (st - sr) / st

    # Generar gráfico
    plt.figure(figsize=(6, 4))
    plt.scatter(x, y, color='blue', label='Datos originales')
    plt.plot(x, y_cal, color='red', label=f'Regresión: {equation}')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Regresión {tipo.capitalize()}")
    plt.legend()
    plt.grid()

    # Guardar imagen en base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode()

    # Devolver resultados en formato HTML
    tabla_html = f"""
    <p>{equation}</p>
    <p>r² = {r2:.4f}</p>
    <img src="data:image/png;base64,{grafico_base64}" alt="Gráfico de Regresión">
    """

    return tabla_html



