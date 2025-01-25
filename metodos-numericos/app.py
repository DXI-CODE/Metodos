from flask import Flask, render_template, request, jsonify
from calculos.interpolacion import calcular_interpolacion
from calculos.serietaylor import calcular_serie_taylor
from calculos.seriemclaurin import calcular_serie_mclaurin
from calculos.gaussinversa import convertir_matriz_a_html
from calculos.puntofijo import metodo_punto_fijo

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


##______________________________________________

@app.route('/')
def home():
    rutas_get = [
        {"nombre": "Serie de Taylor", "url": "/serie-taylor"},
        {"nombre": "Serie de McLaren", "url": "/serie-mclaurin"},
        {"nombre": "Matriz Inversa", "url": "/matriz-inversa"},
        # AQUI AGREGUEN SUS RUTAS PARA SUS METODOS
    ]
    return render_template('principal/inicio.html', rutas = rutas_get)

##______________________________________________

##METODO DE SERIE DE TAYLOR
@app.route('/serie-taylor', methods=['GET'])
def calcular_taylor_get():
    return render_template('series/serietaylor.html')
@app.route('/serie-taylor', methods=['POST'])
def calcular_taylor_post():
    datos = request.json
    funcion_str = datos.get('funcion')
    expansion = datos.get('expansion')
    numero_n = datos.get('numero_n')

    if not funcion_str or expansion is None or numero_n is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400
    
    try:
        serie = calcular_serie_taylor(funcion_str, expansion, numero_n)
        return jsonify({'resultado_funcion': serie})
    except Exception as e:
        return jsonify({'error': f'Error al calcular la serie de Taylor: {str(e)}'}), 500

##______________________________________________


#METODO DE SERIE DE MC LAURIN
@app.route('/serie-mclaurin', methods=['GET'])
def calcular_mclaurin_get():
    return render_template('series/seriemclaurin.html')
@app.route('/serie-mclaurin', methods=['POST'])
def calcular_mclaurin_post():
    datos = request.json
    funcion_str = datos.get('funcion')
    numero_n = datos.get('numero_n')

    if funcion_str is None or numero_n is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        resultado = calcular_serie_mclaurin(funcion_str, numero_n) 
        print(resultado)

        return jsonify({'resultado_funcion': resultado})

    except Exception as e:
        return jsonify({'error': f'Error al calcular la serie de mclaurin: {str(e)}'}), 500

##______________________________________________



##______________________________________________

##METODO DE MATRIZ INVERSA

@app.route('/matriz-inversa', methods=['GET'])
def calcular_gauss_inversa_get():
    return render_template('Matrices/GaussInversa.html')
@app.route('/matriz-inversa', methods=['POST'])
def calcular_gauss_inversa_post():
    datos = request.json 
    matriz = datos.get('matrix')  
    if not matriz:
        return jsonify({'error': 'Se requiere una matriz válida.'}), 400

    try:
        ##matriz_np = np.array(matriz, dtype=float)

        ##if matriz_np.shape[0] != matriz_np.shape[1]:
        ##    return jsonify({'error': 'La matriz debe ser cuadrada.'}), 400
        
        inversa = np.linalg.inv(matriz_np)
        inversa_html = convertir_matriz_a_html(inversa)
        return jsonify({'matriz_inversa_html': inversa_html})
    except np.linalg.LinAlgError:
        return jsonify({'error': 'La matriz no es invertible.'}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la matriz inversa: {str(e)}'}), 500
    
##______________________________________________


##______________________________________________
##METODO DE PUNTO FIJO

@app.route('/metodo-punto-fijo', methods=['GET'])
def calcular_punto_fijo_get():
    return render_template('MetodosEcuacionesNoLineales/MetodoPuntoFijo.html')
@app.route('/metodo-punto-fijo', methods=['POST'])
def calcular_punto_fijo_post():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        x0 = float(data.get('x0'))
        tolerancia = float(data.get('tolerancia'))
        iteraciones_max = int(data.get('iteraciones'))

        resultado = metodo_punto_fijo(funcion_str, x0, tolerancia, iteraciones_max)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"})

##______________________________________________

    
if __name__ == '__main__':
    app.run(debug=True)
