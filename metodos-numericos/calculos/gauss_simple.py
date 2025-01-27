import numpy as np

def validar_matriz(matriz):
    try:
        matriz_np = np.array(matriz, dtype=float)
        if matriz_np.shape[0] + 1 != matriz_np.shape[1]:
            return "La matriz debe ser aumentada (n x n+1).", 400
        return matriz_np, None
    except ValueError:
        return "Los elementos de la matriz deben ser numéricos.", 400

def gauss_simple(matriz):
    try:
        n = len(matriz)
        for i in range(n):
            # Pivoteo parcial
            max_fila = np.argmax(abs(matriz[i:, i])) + i
            matriz[[i, max_fila]] = matriz[[max_fila, i]]

            # Eliminación
            for j in range(i+1, n):
                factor = matriz[j, i] / matriz[i, i]
                matriz[j, i:] -= factor * matriz[i, i:]

        # Extraer las soluciones
        soluciones = np.zeros(n)
        for i in range(n-1, -1, -1):
            suma = sum(matriz[i, i+1:n] * soluciones[i+1:n])
            soluciones[i] = (matriz[i, -1] - suma) / matriz[i, i]

        matriz_html = convertir_matriz_a_html(matriz)
        return {"soluciones": soluciones.tolist(), "matriz_html": matriz_html}, None
    except Exception as e:
        return f"Error en el cálculo: {str(e)}", 500

    


def convertir_matriz_a_html(matriz):
    """Convierte una matriz numpy a formato HTML."""
    html = "<table border='1' style='border-collapse: collapse; text-align: center;'>"
    for row in matriz:
        html += "<tr>" + "".join(f"<td>{elem:.2f}</td>" for elem in row) + "</tr>"
    html += "</table>"
    return html
