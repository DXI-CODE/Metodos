import numpy as np

def validar_matriz(matriz):
    """Función para validar que la matriz sea cuadrada y tenga datos válidos."""
    if not matriz:
        return {'error': 'Se requiere una matriz válida.'}, 400

    matriz_np = np.array(matriz, dtype=float)

    if matriz_np.shape[0] != matriz_np.shape[1]:
        return {'error': 'La matriz debe ser cuadrada.'}, 400

    return matriz_np, None

def calcular_inversa(matriz_np):
    """Función para calcular la inversa de la matriz."""
    try:
        inversa = np.linalg.inv(matriz_np)
        inversa_html = convertir_matriz_a_html(inversa)
        return {'resultado_matriz': inversa_html}, None
    except np.linalg.LinAlgError:
        return {'error': 'La matriz no es invertible.'}, 400
    except Exception as e:
        return {'error': f'Error al calcular la matriz inversa: {str(e)}'}, 500

def convertir_matriz_a_html(matriz):
    """Función para convertir la matriz numpy a HTML."""
    html = "<table>"
    for row in matriz:
        html += "<tr>" + "".join(f"<td>{elem:.2f}</td>" for elem in row) + "</tr>"
    html += "</table>"
    return html
