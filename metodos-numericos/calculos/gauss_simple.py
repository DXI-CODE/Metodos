import numpy as np

def validar_matriz_aumentada(matriz):
    """Valida que la matriz aumentada sea correcta para Gauss-Jordan simple."""
    if not matriz:
        return {'error': 'Se requiere una matriz válida.'}, 400

    matriz_np = np.array(matriz, dtype=float)

    filas, columnas = matriz_np.shape
    if columnas != filas + 1:
        return {'error': 'La matriz aumentada debe tener n filas y n+1 columnas.'}, 400

    return matriz_np, None

def gauss_jordan_simple(matriz_np):
    """Aplica el método de Gauss-Jordan simple a la matriz aumentada."""
    try:
        filas, columnas = matriz_np.shape

        for i in range(filas):
            # Seleccionar el pivote y verificar que no sea cero
            if matriz_np[i, i] == 0:
                return {'error': 'El sistema no tiene solución única (pivote cero).'}, 400

            # Hacer ceros debajo del pivote
            for j in range(i + 1, filas):
                factor = matriz_np[j, i] / matriz_np[i, i]
                matriz_np[j] = matriz_np[j] - factor * matriz_np[i]

        return {'matriz_escalonada': convertir_matriz_a_html(matriz_np)}, None

    except Exception as e:
        return {'error': f'Error al aplicar Gauss-Jordan simple: {str(e)}'}, 500

def convertir_matriz_a_html(matriz):
    """Función para convertir la matriz numpy a HTML."""
    html = "<table>"
    for row in matriz:
        html += "<tr>" + "".join(f"<td>{elem:.2f}</td>" for elem in row) + "</tr>"
    html += "</table>"
    return html
