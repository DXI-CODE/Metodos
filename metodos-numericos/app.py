from flask import Flask, render_template, request, jsonify
from calculos.interpolacion import calcular_interpolacion
from calculos.serietaylor import calcular_serie_taylor
from calculos.seriemclaurin import calcular_serie_mclaurin
from calculos.gaussinversa import validar_matriz, calcular_inversa
from calculos.puntofijo import metodo_punto_fijo
from calculos.simpson3_8 import calcular_simpson_3_8
from calculos.linealizacioncrecimiento import metodo_linealizacion_crecimiento
from calculos.interpolacionlagrange import lagrange
from calculos.regresionmultilineal import calcular_regresion
from calculos.simpson1_3 import simpson1_3
from calculos.falsaposicion import calcular_falsa_posicion

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
        {"nombre": "Metodo Simpson 3/8", "url": "/metodo-simpson-3_8"},
        {"nombre": "Linealizacion a razon de crecimiento", "url":"/linealizacion-a-razon-crecimiento"},
        {"nombre": "Regresion multilineal", "url":"/regresion-multilineal"},
        {"nombre": "Integración por Simpson 1_3", "url":"/simpson1_3"},
        {"nombre": "Metodo Falsa Posicion", "url":"metodos_raices/falsaposicion.html"},
        # AQUI AGREGUEN SUS RUTAS PARA SUS METODOS
    ]
    return render_template('principal/inicio.html', rutas = rutas_get)

##______________________________________________


##[

    ##METODOS DE JOAN

##]


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


## METODO DE FALSA POSICIÓN

##______________________________________________
@app.route('/metodo-falsa-posicion', methods=['GET'])
def calcular_falsa_posicion_get():
    return render_template('metodos_raices/falsaposicion.html')

@app.route('/metodo-falsa-posicion', methods=['POST'])
def calcular_falsa_posicion_post():
    datos = request.json
    funcion_str = datos.get('funcion')
    valor_a = float(datos.get('valor_a'))
    valor_b = float(datos.get('valor_b'))
    tolerancia = float(datos.get('tolerancia'))
    iteraciones = int(datos.get('iteraciones'))

    if not funcion_str or valor_a is None or valor_b is None or tolerancia is None or iteraciones is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        resultados = calcular_falsa_posicion(funcion_str, valor_a, valor_b, tolerancia, iteraciones)
        return jsonify({'resultados': resultados})

    except Exception as e:
        return jsonify({'error': f'Error al calcular el método de Falsa Posición: {str(e)}'}), 500



##______________________________________________

##[

    ##METODOS DE JEOVANI

##]


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


##[

    ##METODOS DE JEYCSON

##]


##______________________________________________
##LINEALIZACION A RAZON DE CRECIMIENTO
@app.route('/linealizacion-a-razon-crecimiento', methods=['GET'])
def calcular_linealizacion_razon_crecimiento_get():
    return render_template('Linealizacion/RazonCrecimiento.html')
@app.route('/linealizacion-a-razon-crecimiento', methods=['POST'])
def calcular_linealizacion_razon_crecimiento_post():
    try:
        data = request.get_json()
        datos = data.get('valores')

        resultado = metodo_linealizacion_crecimiento(datos)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"})

##______________________________________________
   
#METODO DE INTERPOLACION DE LAGRANGE

@app.route('/calcular_lagrange', methods=['GET'])
def calcular_lagrange_get():
    return render_template('interpolacion/lagrange.html')
@app.route('/calcular_lagrange', methods=['POST'])
def calcular_lagrange_post():
    datos = request.json
    puntos = datos.get('puntos')
    grado = datos.get('grado')
    valorx = datos.get('valorx')

    if not puntos or grado is None or valorx is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        serie = lagrange(puntos, grado, valorx)
        return jsonify({'funcion': serie})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la interpolación de Lagrange: {str(e)}'}), 500

##______________________________________________
    
##______________________________________________
##METODO DE SIMPSON 3/8

@app.route('/metodo-simpson-3_8', methods=['GET'])
def metodo_simpson_38_get():
    return render_template('Integracion/Simpson3-8.html')
@app.route('/metodo-simpson-3_8', methods=['POST'])
def metodo_simpson_38_post():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        limite_inferior = float(data.get('limite_inferior'))
        limite_superior = float(data.get('limite_superior'))
        subintervalos = int(data.get('subintervalos'))

        resultado = calcular_simpson_3_8(funcion_str, limite_inferior, limite_superior, subintervalos)
        return jsonify({"resultado_num": resultado})

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"})

##______________________________________________
    
    
##______________________________________________
##REGRESION MULTILINEAL
@app.route('/regresion-multilineal', methods=['GET'])
def regresion_multilineal_get():
    return render_template('Regresion/RegresionMultilineal.html')
@app.route("/regresion-multilineal", methods=["POST"])
def regresion_multilineal():
    data = request.get_json()  
    X = data.get("X")  
    y = data.get("y")
    resultado = calcular_regresion(X, y)
    if "error" in resultado:
        return jsonify({"error": resultado["error"]})

    coeficientes = resultado["coeficientes"]
    intercepto = resultado["intercepto"]
    ecuacion = " + ".join([f"{coef:.6f}*x{i+1}" for i, coef in enumerate(coeficientes) if coef >= 0])
    ecuacion += " " + " ".join([f"{coef:.6f}*x{i+1}" for i, coef in enumerate(coeficientes) if coef < 0])
    ecuacion += f" + {intercepto:.6f}"

    return jsonify({
        'ecuacion': ecuacion,
        'coeficientes': coeficientes,
        'intercepto': intercepto
    })
##______________________________________________

##______________________________________________
        
#METODO DE INTEGRACIÓN POR SIMPSON 1/3  

@app.route('/simpson1_3', methods=['GET'])
def calcular_simpson1_3_get():
    return render_template('Integracion/Simpson1_3.html')
@app.route('/simpson1_3', methods=['POST'])
def calcular_simpson1_3_post():
    datos = request.json
    funcion = datos.get('funcion')
    x0 = datos.get('x0')
    xn = datos.get('xn')
    numero_n = datos.get('numero_n')
    

    if not funcion or x0 is None or xn is None or numero_n is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        simpson = simpson1_3(funcion, x0, xn, numero_n)
        return jsonify({'funcion': simpson})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la integración por Simpson 1/3: {str(e)}'}), 500

##______________________________________________

if __name__ == '__main__':
    app.run(debug=True,  host='127.0.0.1', port=5000)
