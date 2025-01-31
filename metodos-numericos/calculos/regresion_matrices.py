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
        
        # Formatear la ecuación correctamente
        a0 = coef[0]
        a1 = coef[1]
        if a1 < 0:
            equation = f"y = {a0:.4f} - {abs(a1):.4f}x"
        else:
            equation = f"y = {a0:.4f} + {a1:.4f}x"
    
    elif tipo == 'cuadratica':
        A = np.vstack([np.ones_like(x), x, x**2]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        y_cal = A @ coef
        
        # Formatear la ecuación correctamente
        a0 = coef[0]
        a1 = coef[1]
        a2 = coef[2]
        
        if a1 < 0 and a2 < 0:
            equation = f"y = {a0:.4f} - {abs(a1):.4f}x - {abs(a2):.4f}x²"
        elif a1 < 0:
            equation = f"y = {a0:.4f} - {abs(a1):.4f}x + {a2:.4f}x²"
        elif a2 < 0:
            equation = f"y = {a0:.4f} + {a1:.4f}x - {abs(a2):.4f}x²"
        else:
            equation = f"y = {a0:.4f} + {a1:.4f}x + {a2:.4f}x²"
    
    elif tipo == 'cubica':
        A = np.vstack([np.ones_like(x), x, x**2, x**3]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        y_cal = A @ coef
        
        # Formatear la ecuación correctamente
        a0 = coef[0]
        a1 = coef[1]
        a2 = coef[2]
        a3 = coef[3]
        
        if a1 < 0 and a2 < 0 and a3 < 0:
            equation = f"y = {a0:.4f} - {abs(a1):.4f}x - {abs(a2):.4f}x² - {abs(a3):.4f}x³"
        elif a1 < 0 and a2 < 0:
            equation = f"y = {a0:.4f} - {abs(a1):.4f}x - {abs(a2):.4f}x² + {a3:.4f}x³"
        elif a1 < 0 and a3 < 0:
            equation = f"y = {a0:.4f} - {abs(a1):.4f}x + {a2:.4f}x² - {abs(a3):.4f}x³"
        elif a2 < 0 and a3 < 0:
            equation = f"y = {a0:.4f} + {a1:.4f}x - {abs(a2):.4f}x² - {abs(a3):.4f}x³"
        elif a1 < 0:
            equation = f"y = {a0:.4f} - {abs(a1):.4f}x + {a2:.4f}x² + {a3:.4f}x³"
        elif a2 < 0:
            equation = f"y = {a0:.4f} + {a1:.4f}x - {abs(a2):.4f}x² + {a3:.4f}x³"
        elif a3 < 0:
            equation = f"y = {a0:.4f} + {a1:.4f}x + {a2:.4f}x² - {abs(a3):.4f}x³"
        else:
            equation = f"y = {a0:.4f} + {a1:.4f}x + {a2:.4f}x² + {a3:.4f}x³"

    # Calcular R²
    st = np.sum((y - np.mean(y))**2)
    sr = np.sum((y - y_cal)**2)
    r2 = (st - sr) / st

    # Crear tabla HTML
    tabla_html = """
    <table border="1">
        <tr>
            <th>x</th><th>y</th><th>x²</th><th>xy</th><th>ŷ</th><th>St</th><th>Sr</th>
        </tr>
    """

    for i in range(len(x)):
        st_i = (y[i] - np.mean(y))**2
        sr_i = (y[i] - y_cal[i])**2
        tabla_html += f"""
        <tr>
            <td>{x[i]:.4f}</td><td>{y[i]:.4f}</td><td>{x[i]**2:.4f}</td>
            <td>{x[i] * y[i]:.4f}</td><td>{y_cal[i]:.4f}</td>
            <td>{st_i:.4f}</td><td>{sr_i:.4f}</td>
        </tr>
        """

    # Agregar la suma de las columnas
    tabla_html += f"""
        <tr>
            <td><b>Σ</b></td><td>{np.sum(y):.4f}</td><td>{np.sum(x**2):.4f}</td>
            <td>{np.sum(x * y):.4f}</td><td>-</td><td>{st:.4f}</td><td>{sr:.4f}</td>
        </tr>
    </table>
    """

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
    resultado_html = f"""
    <p>{equation}</p>
    <p>r² = {r2:.4f}</p>
    <img src="data:image/png;base64,{grafico_base64}" alt="Gráfico de Regresión">
    <p>Tabla de Resultados:</p>
    {tabla_html}
    """

    return resultado_html
