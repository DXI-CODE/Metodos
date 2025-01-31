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

    # Crear tabla HTML
    tabla_html = """
    <table border="1">
        <tr>
            <th>x</th><th>y</th><th>x²</th><th>xy</th><th>ŷ</th><th>St</th><th>Sr</th>
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
    
    tabla_html += f"""
        <tr>
            <td><b>Σ</b></td><td>{sum_y:.4f}</td><td>{sum_x2:.4f}</td>
            <td>{sum_xy:.4f}</td><td>-</td><td>{st:.4f}</td><td>{sr:.4f}</td>
        </tr>
    </table>
    <div class="texto box">
        <p>a0 = {a0:.4f}</p>
        <p>a1 = {a1:.4f}</p>
        <p>St = {st:.4f}</p>
        <p>Sr = {sr:.4f}</p>
        <p>r² = {r2:.4f}</p>
    </div>
    """

    # Formateo de la ecuación para mostrar correctamente el signo de a1
    if a1 < 0:
        a1_str = f"- {abs(a1):.4f}"
    else:
        a1_str = f"+ {a1:.4f}"

    # Generar gráfico
    plt.figure(figsize=(6, 4))
    plt.scatter(x, y, color='blue', label='Datos originales')
    plt.plot(x, y_cal, color='red', linestyle='-', label=f'Regresión: y = {a0:.4f} {a1_str}x')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Regresión Lineal")
    plt.legend()
    plt.grid()

    # Guardar imagen en base64 para enviarla al HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode()

    return tabla_html, grafico_base64
