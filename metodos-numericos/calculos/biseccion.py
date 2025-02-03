import math
import matplotlib.pyplot as plt
import io
import base64

# Función matemática para la cual se calcula la raíz
def f(c, g, m, t, v):
    """Función para la cual se calcula la raíz."""
    return (g * m / c) * (1 - math.exp(-c * t / m)) - v

# Método de Bisección
def biseccion(f, xl, xu, tol, max_iter, g, m, t, v):
    """Método de Bisección para encontrar la raíz de una función."""
    iteraciones = 0
    xr = (xl + xu) / 2.0
    resultados = []
    xr_values = []  # Para almacenar los valores de xr en cada iteración

    while abs(f(xr, g, m, t, v)) > tol and iteraciones < max_iter:
        xr = (xl + xu) / 2.0
        resultado = {
            'iteracion': iteraciones + 1,
            'xl': xl,
            'xu': xu,
            'xr': xr,
            'f_xl': f(xl, g, m, t, v),
            'f_xu': f(xu, g, m, t, v),
            'f_xr': f(xr, g, m, t, v)
        }
        resultados.append(resultado)
        xr_values.append(xr)  # Guardar el valor de xr para la gráfica

        # Actualizar los límites del intervalo
        if f(xl, g, m, t, v) * f(xr, g, m, t, v) < 0:
            xu = xr
        else:
            xl = xr

        iteraciones += 1

    # Generar la gráfica
    plt.figure()
    plt.plot(range(1, iteraciones + 1), xr_values, marker='o', linestyle='-', color='b')
    plt.title('Convergencia del Método de Bisección')
    plt.xlabel('Iteración')
    plt.ylabel('xr')
    plt.grid(True)

    # Guardar la gráfica en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Convertir la gráfica a base64 para enviarla al frontend
    grafica_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return {
        'raiz': xr,
        'iteraciones': iteraciones,
        'resultados': resultados,
        'grafica': grafica_base64  # Agregar la gráfica en base64
    }

# Convertir resultados a una tabla HTML
def convertir_resultados_a_html(resultados):
    """Convierte los resultados de las iteraciones a una tabla HTML."""
    html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    html += "<tr><th>Iteración</th><th>xl</th><th>xu</th><th>xr</th><th>f(xl)</th><th>f(xu)</th><th>f(xr)</th></tr>"
    for res in resultados:
        html += (
            f"<tr>"
            f"<td>{res['iteracion']}</td>"
            f"<td>{res['xl']:.6f}</td>"
            f"<td>{res['xu']:.6f}</td>"
            f"<td>{res['xr']:.6f}</td>"
            f"<td>{res['f_xl']:.6f}</td>"
            f"<td>{res['f_xu']:.6f}</td>"
            f"<td>{res['f_xr']:.6f}</td>"
            f"</tr>"
        )
    html += "</table>"
    return html