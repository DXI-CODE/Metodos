import numpy as np

def validar_matriz_aumentada(matriz):
    """Valida que la matriz aumentada sea correcta para Gauss-Jordan simple."""
    if matriz is None or not isinstance(matriz, list) or not matriz:
        return {'error': 'Se requiere una matriz válida.'}, 400

    try:
        matriz_np = np.array(matriz, dtype=float)
    except ValueError:
        return {'error': 'Todos los elementos de la matriz deben ser números.'}, 400

    filas, columnas = matriz_np.shape
    if columnas != filas + 1:
        return {'error': 'La matriz aumentada debe tener n filas y n+1 columnas.'}, 400

    return matriz_np, None

def gauss_jordan_simple(matriz_np):
    """Aplica el método de Gauss-Jordan simple a la matriz aumentada."""
    try:
        filas, columnas = matriz_np.shape

        for i in range(filas):
            # Pivoteo parcial para evitar divisiones entre cero
            if matriz_np[i, i] == 0:
                for k in range(i + 1, filas):
                    if matriz_np[k, i] != 0:
                        matriz_np[[i, k]] = matriz_np[[k, i]]  # Intercambiar filas
                        break
                else:
                    return {'error': 'El sistema no tiene solución única (pivote cero).'}, 400

            # Normalizar el pivote
            matriz_np[i] = matriz_np[i] / matriz_np[i, i]

            # Hacer ceros en las demás filas
            for j in range(filas):
                if i != j:
                    factor = matriz_np[j, i]
                    matriz_np[j] = matriz_np[j] - factor * matriz_np[i]

        return {'matriz_resultante': convertir_matriz_a_html(matriz_np)}, None

    except Exception as e:
        return {'error': f'Error al aplicar Gauss-Jordan simple: {str(e)}'}, 500

def convertir_matriz_a_html(matriz):
    """Función para convertir la matriz numpy a HTML."""
    html = "<table style='border-collapse: collapse; text-align: center;'>"
    for row in matriz:
        html += "<tr>" + "".join(f"<td style='border: 1px solid black; padding: 5px;'>{elem:.2f}</td>" for elem in row) + "</tr>"
    html += "</table>"
    return html
