from flask import Flask, render_template, request, jsonify
from calculos.interpolacion import calcular_interpolacion
from calculos.serietaylor import calcular_serie_taylor
from calculos.seriemclaurin import calcular_serie_mclaurin
from calculos.gaussinversa import validar_matriz, calcular_inversa
from calculos.puntofijo import metodo_punto_fijo

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


##______________________________________________
##PAGINA DE INICIO
@app.route('/')
def home():
    rutas_get = [
        {"nombre": "Serie de Taylor", "url": "/serie-taylor"},
        {"nombre": "Serie de McLaren", "url": "/serie-mclaurin"},
        {"nombre": "Matriz Inversa", "url": "/matriz_inversa"},
        {"nombre": "Metodo Punto Fijo", "url": "/metodo-punto-fijo"},
        {"nombre": "Linealizacion a razon de crecimiento", "url":"/linealizacion-a-razon-crecimiento"},
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

@app.route('/matriz_inversa', methods=['GET'])
def calcular_gauss_inversa_get():
    return render_template('Matrices/GaussInversa.html')
@app.route('/matriz_inversa', methods=['POST'])
def calcular_gauss_inversa_post():
    datos = request.json
    matriz = datos.get('matrix') 

    matriz_np, error = validar_matriz(matriz)
    if error:
        return jsonify(matriz_np), error

    resultado, error = calcular_inversa(matriz_np)
    if error:
        return jsonify(resultado), error

    return jsonify(resultado)
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

##______________________________________________
##LINEALIZACION A RAZON DE CRECIMIENTO
@app.route('/linealizacion-a-razon-crecimiento', methods=['GET'])
def calcular_linealizacion_razon_crecimiento_get():
    return render_template('Linealizacion/RazonCrecimiento.html')
@app.route('/linealizacion-a-razon-crecimiento', methods=['POST'])
def calcular_linealizacion_razon_crecimiento_post():
    try:
        data = request.get_json()
        datos = data.get('data')

        resultado = metodo_linealizacion_crecimiento(datos)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"})


    
if __name__ == '__main__':
    app.run(debug=True)
