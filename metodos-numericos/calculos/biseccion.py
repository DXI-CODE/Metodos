import math
import matplotlib.pyplot as plt
import io
import base64

def f(c, g, m, t, v):
    """Función para la cual se calcula la raíz."""
    return (g * m / c) * (1 - math.exp(-c * t / m)) - v

def biseccion(f, xl, xu, tol, max_iter, g, m, t, v):
    """Método de Bisección para encontrar la raíz de una función."""
    iteraciones = 0
    xr = (xl + xu) / 2.0
    resultados = []
    x_values = []  # Para almacenar los valores de xr en cada iteración

    while abs(f(xr, g, m, t, v)) > tol and iteraciones < max_iter:
        xr = (xl + xu) / 2.0
        resultado = {
            'iteracion': iteraciones + 1,
            'xl': xl,
            'xu': xu,
            'xr': xr
        }
        resultados.append(resultado)
        x_values.append(xr)

        if f(xl, g, m, t, v) * f(xr, g, m, t, v) < 0:
            xu = xr
        else:
            xl = xr
        
        iteraciones += 1

    # Generar la gráfica
    grafica_url = generar_grafica(x_values)

    return {
        'raiz': xr,
        'iteraciones': iteraciones,
        'resultados': resultados,
        'grafica': grafica_url  # Se agrega la URL de la gráfica en base64
    }

def generar_grafica(x_values):
    """Genera la gráfica de convergencia y la convierte en base64."""
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

def convertir_resultados_a_html(resultados):
    """Convierte los resultados de las iteraciones a una tabla HTML."""
    html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    html += "<tr><th>Iteración</th><th>xl</th><th>xu</th><th>xr</th></tr>"
    for res in resultados:
        html += (
            f"<tr>"
            f"<td>{res['iteracion']}</td>"
            f"<td>{res['xl']:.6f}</td>"
            f"<td>{res['xu']:.6f}</td>"
            f"<td>{res['xr']:.6f}</td>"
            f"</tr>"
        )
    html += "</table>"
    return html
