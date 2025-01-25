from flask import Flask, render_template, request, jsonify
import numpy as sp
import numpy as np
from calculos.interpolacion import calcular_interpolacion
from calculos.serietaylor import calcular_serie_taylor
from calculos.seriemclaren import calcular_serie_mclaren
from calculos.gaussinversa import convertir_matriz_a_html

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Matrices/GaussInversa.html')   ##SI REQUIEREN PROBAR SUS METODOS CAMBIEN EL NOMBRE DE LA RUTA


##METODO DE SERIE DE TAYLOR
@app.route('/calcular_taylor', methods=['GET'])
def calcular_taylor_get():
    return render_template('series/SerieTaylor.html')
@app.route('/calcular_taylor', methods=['POST'])
def calcular_taylor_post():
    datos = request.json
    funcion_str = datos.get('funcion')
    expansion = datos.get('expansion')
    numero_n = datos.get('numero_n')

    if not funcion_str or expansion is None or numero_n is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400
    
    try:
        serie = calcular_serie_taylor(funcion_str, expansion, numero_n)
        return jsonify({'funcion_taylor': serie})
    except Exception as e:
        return jsonify({'error': f'Error al calcular la serie de Taylor: {str(e)}'}), 500

#METODO DE SERIE DE MCLAREN
@app.route('/calcular_mclaren', methods=['GET'])
def calcular_mclaren_get():
    return render_template('series/SerieMcLaren.html')
@app.route('/calcular_mclaren', methods=['POST'])
def calcular_mclaren_post():
    datos = request.json
    funcion_str = datos.get('funcion')
    expansion = datos.get('expansion')
    numero_n = datos.get('numero_n')

    if not funcion_str or expansion is None or numero_n is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        expansion = float(expansion) 
        numero_n = int(numero_n)  

        x = sp.symbols('x')
        funcion = sp.sympify(funcion_str)

        serie_taylor = sp.series(funcion, x, expansion, numero_n)
        serie_formateada = str(serie_taylor).replace('**', '^').replace('O(', 'O(')

        return jsonify({'funcion_taylor': serie_formateada})

    except Exception as e:
        return jsonify({'error': f'Error al calcular la serie de McLaren: {str(e)}'}), 500


@app.route('/calcular_inversa', methods=['GET'])
def calcular_gauss_inversa_get():
    return render_template('Matrices/GaussInversa.html')
@app.route('/calcular_inversa', methods=['POST'])
def calcular_gauss_inversa_post():
    datos = request.json 
    matriz = datos.get('matrix')  
    if not matriz:
        return jsonify({'error': 'Se requiere una matriz válida.'}), 400

    try:
        matriz_np = np.array(matriz, dtype=float)

        if matriz_np.shape[0] != matriz_np.shape[1]:
            return jsonify({'error': 'La matriz debe ser cuadrada.'}), 400
        
        inversa = np.linalg.inv(matriz_np)
        inversa_html = convertir_matriz_a_html(inversa)
        return jsonify({'matriz_inversa_html': inversa_html})
    except np.linalg.LinAlgError:
        return jsonify({'error': 'La matriz no es invertible.'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la matriz inversa: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
