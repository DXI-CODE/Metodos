import numpy as np

def validar_matriz_aumentada(matriz):
    if not matriz:
        return {'error': 'Se requiere una matriz válida.'}, 400

    try:
        matriz_np = np.array(matriz, dtype=float)
    except ValueError as e:
        return {'error': 'Los valores de la matriz deben ser números válidos.'}, 400

    filas, columnas = matriz_np.shape
    if columnas != filas + 1:  # Verifica si es una matriz aumentada
        return {'error': 'La matriz debe ser una matriz aumentada (n x n+1).'}, 400

    return matriz_np, None

def gauss_simple(matriz_np):
    try:
        filas, columnas = matriz_np.shape
        for i in range(filas):
            # Hacer el pivote 1
            pivote = matriz_np[i][i]
            if pivote == 0:
                return {'error': 'Se encontró un pivote cero, la matriz no se puede resolver con Gauss Simple.'}, 400
            matriz_np[i] = matriz_np[i] / pivote

            # Hacer ceros debajo del pivote
            for j in range(i + 1, filas):
                matriz_np[j] -= matriz_np[i] * matriz_np[j][i]

        # Extraer soluciones
        soluciones = matriz_np[:, -1]
        matriz_escalonada = convertir_matriz_a_html(matriz_np)

        return {'soluciones': soluciones.tolist(), 'matriz_escalonada': matriz_escalonada}, None
    except Exception as e:
        return {'error': f'Error al calcular el método de Gauss Simple: {str(e)}'}, 500

def convertir_matriz_a_html(matriz):
    html = "<table>"
    for row in matriz:
        html += "<tr>" + "".join(f"<td>{elem:.2f}</td>" for elem in row) + "</tr>"
    html += "</table>"
    return html