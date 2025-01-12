from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('interpolacion/index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    datos = request.json
    puntos = datos.get('puntos')  # Lista de pares de puntos [(x1, y1), (x2, y2), ...]

    if not puntos or len(puntos) < 2:
        return jsonify({'error': 'Se necesitan al menos dos puntos para la interpolación.'}), 400

    try:
        # Validar que cada punto sea una lista de dos números
        if not all(isinstance(p, list) and len(p) == 2 for p in puntos):
            return jsonify({'error': 'Cada punto debe ser una lista de dos números (x, y).'}), 400

        # Validar que todos los valores sean numéricos
        if not all(isinstance(coord, (int, float)) for p in puntos for coord in p):
            return jsonify({'error': 'Todos los valores de los puntos deben ser numéricos.'}), 400

        x_vals = np.array([p[0] for p in puntos])  # Extraer valores de x
        y_vals = np.array([p[1] for p in puntos])  # Extraer valores de y

        # Verificar que no haya valores duplicados en X
        if len(set(x_vals)) != len(x_vals):
            return jsonify({'error': 'Los valores de X deben ser únicos.'}), 400

        # Construir la matriz de Vandermonde
        vandermonde = np.vander(x_vals, increasing=True)

        # Resolver el sistema de ecuaciones Ax = b
        coeficientes = np.linalg.solve(vandermonde, y_vals)

        # Construir el polinomio como una cadena
        terms = [f"{coef:.4f}*x**{i}" for i, coef in enumerate(coeficientes)]
        polinomio = " + ".join(terms)

        return jsonify({'funcion': polinomio})

    except np.linalg.LinAlgError as e:
        return jsonify({'error': 'El sistema no tiene solución única: los puntos pueden ser colineales o no bien definidos.'}), 400
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
