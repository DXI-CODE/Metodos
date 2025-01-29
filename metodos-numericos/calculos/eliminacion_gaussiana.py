<<<<<<< Updated upstream
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

def eliminacion_gaussiana(matriz_np):
    """Aplica el método de eliminación gaussiana para resolver el sistema de ecuaciones."""
    try:
        filas, columnas = matriz_np.shape
        
        # Eliminación hacia adelante
        for i in range(filas - 1):
            if matriz_np[i, i] == 0:
                return {'error': 'No se puede dividir entre cero en la fila.'}, 400
            
            for k in range(i + 1, filas):
                factor = matriz_np[k, i] / matriz_np[i, i]
                for j in range(i, columnas):
                    matriz_np[k, j] -= factor * matriz_np[i, j]
        
        # Sustitución hacia atrás
        soluciones = np.zeros(filas)
        for i in range(filas - 1, -1, -1):
            suma = sum(matriz_np[i, j] * soluciones[j] for j in range(i + 1, filas))
            soluciones[i] = (matriz_np[i, -1] - suma) / matriz_np[i, i]
        
        resultado_html = convertir_vector_a_html(soluciones)
        return {'resultado_matriz': resultado_html}, None
    except Exception as e:
        return {'error': f'Error en eliminación gaussiana: {str(e)}'}, 500

def convertir_vector_a_html(vector):
    """Convierte un vector de soluciones en formato HTML."""
    html = "<h2>Soluciones:</h2><ul>"
    for i, val in enumerate(vector[:3]):  # Solo mostrar x1, x2 y x3
        html += f"<li>x{i + 1} = {val:.4f}</li>"
    html += "</ul>"
    return html
=======
from flask import Flask, request, jsonify, render_template


# Función para resolver la matriz usando eliminación de Gauss
def gaussiana_eliminacion(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    # Eliminación hacia adelante
    for i in range(filas - 1):
        for k in range(i + 1, filas):
            factor = matriz[k][i] / matriz[i][i]
            for j in range(i, columnas):
                matriz[k][j] -= factor * matriz[i][j]

    # Sustitución hacia atrás para encontrar las soluciones
    soluciones = [0] * filas
    for i in range(filas - 1, -1, -1):
        suma = sum(matriz[i][j] * soluciones[j] for j in range(i + 1, columnas - 1))
        soluciones[i] = (matriz[i][columnas - 1] - suma) / matriz[i][i]

    return soluciones



# Ruta para recibir y resolver la matriz enviada desde el formulario HTML

def resolver_gauss():
    try:
        datos = request.json
        matriz = datos['matriz']

        soluciones = gaussiana_eliminacion(matriz)
        return jsonify({'soluciones': soluciones})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

>>>>>>> Stashed changes
