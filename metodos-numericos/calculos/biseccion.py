import math

def f(c, g, m, t, v):
    """Función para la cual se calcula la raíz."""
    return (g * m / c) * (1 - math.exp(-c * t / m)) - v

def biseccion(f, xl, xu, tol, max_iter, g, m, t, v):
    """Método de Bisección para encontrar la raíz de una función."""
    iteraciones = 0
    xr = (xl + xu) / 2.0
    resultados = []
    
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
        
        if f(xl, g, m, t, v) * f(xr, g, m, t, v) < 0:
            xu = xr
        else:
            xl = xr
        
        iteraciones += 1

    return {
        'raiz': xr,
        'iteraciones': iteraciones,
        'resultados': resultados
    }

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
