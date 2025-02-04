import numpy as np

def validar_matriz(matriz):
    """Valida que la matriz sea cuadrada y aumentada correctamente."""
    if not matriz:
        return {'error': 'Se requiere una matriz válida.'}, 400

    matriz_np = np.array(matriz, dtype=float)

    # La matriz debe ser rectangular (n filas, n+1 columnas para el sistema aumentado)
    if matriz_np.shape[0] + 1 != matriz_np.shape[1]:
        return {'error': 'La matriz debe ser aumentada con n filas y n+1 columnas.'}, 400

    return matriz_np, None


def calcular_gauss_jordan(matriz_np):
    """Aplica el método de Gauss-Jordan para resolver el sistema."""
    try:
        filas, columnas = matriz_np.shape
        for i in range(filas):
            # Hacer que el pivote sea 1
            pivote = matriz_np[i, i]
            if pivote == 0:
                return {'error': 'No se puede dividir entre cero en la fila.'}, 400
            matriz_np[i] = matriz_np[i] / pivote

            # Hacer ceros en la columna del pivote para las demás filas
            for j in range(filas):
                if i != j:
                    factor = matriz_np[j, i]
                    matriz_np[j] = matriz_np[j] - factor * matriz_np[i]

        resultado_html = convertir_matriz_a_html(matriz_np)
        return {'resultado_matriz': resultado_html}, None
    except Exception as e:
        return {'error': f'Error al calcular Gauss-Jordan: {str(e)}'}, 500


def convertir_matriz_a_html(matriz):
    """Convierte una matriz numpy a formato HTML."""
    html = "<table>"
    for row in matriz:
        html += "<tr>" + "".join(f"<td>{elem:.2f}</td>" for elem in row) + "</tr>"
    html += "</table>"
    return html
