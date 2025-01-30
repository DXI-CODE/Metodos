import numpy as np
import matplotlib.pyplot as plt
import base64
import io

def regresion_lineal(x, y):
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x2 = np.sum(x**2)
    sum_xy = np.sum(x * y)
    
    # Cálculo de los coeficientes
    A = np.array([[n, sum_x], [sum_x, sum_x2]])
    C = np.array([sum_y, sum_xy])
    a0, a1 = np.linalg.solve(A, C)

    # Cálculo de valores ajustados y errores
    y_cal = a0 + a1 * x
    st = np.sum((y - np.mean(y))**2)  # Suma total de cuadrados
    sr = np.sum((y - y_cal)**2)       # Suma de los residuos al cuadrado
    r2 = (st - sr) / st               # Coeficiente de determinación

    tabla_html = """
    <table border="1">
        <tr>
            <th>x</th><th>y</th><th>x²</th><th>xy</th><th>ŷ (Y_cal)</th><th>St</th><th>Sr</th>
        </tr>
    """
    
    for i in range(n):
        st_i = (y[i] - np.mean(y))**2
        sr_i = (y[i] - y_cal[i])**2
        tabla_html += f"""
        <tr>
            <td>{x[i]:.4f}</td><td>{y[i]:.4f}</td><td>{x[i]**2:.4f}</td>
            <td>{x[i] * y[i]:.4f}</td><td>{y_cal[i]:.4f}</td>
            <td>{st_i:.4f}</td><td>{sr_i:.4f}</td>
        </tr>
        """

    # Agregar totales
    tabla_html += f"""
        <tr>
            <td><strong>Σ</strong></td>
            <td><strong>{sum_y:.4f}</strong></td>
            <td><strong>{sum_x2:.4f}</strong></td>
            <td><strong>{sum_xy:.4f}</strong></td>
            <td>-</td>
            <td><strong>{st:.4f}</strong></td>
            <td><strong>{sr:.4f}</strong></td>
        </tr>
    </table>
    """

    plt.figure(figsize=(8, 6))
    
    # 🔹 **Puntos originales (Azul)**
    plt.scatter(x, y, color='blue', label='Datos originales')

    # 🔹 **Puntos ajustados (Verde)**
    plt.scatter(x, y_cal, color='green', label='Y Calculada', marker='x', s=100)

    # 🔹 **Línea de regresión (Rojo)**
    plt.plot(x, y_cal, color='red', linestyle='--', label='Recta de Regresión')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Regresión Lineal por Mínimos Cuadrados')
    plt.legend()
    plt.grid(True)


    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    
    return tabla_html, f"data:image/png;base64,{grafico_base64}", a0, a1, r2
