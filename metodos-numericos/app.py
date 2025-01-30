from flask import Flask, render_template, request, jsonify, send_file
from calculos.interpolacion import calcular_interpolacion
from calculos.serietaylor import calcular_serie_taylor
from calculos.seriemclaurin import calcular_serie_mclaurin
from calculos.gaussinversa import validar_matriz, calcular_inversa
from calculos.puntofijo import calcular_y_graficar, metodo_punto_fijo_calculo
from calculos.simpson3_8 import calcular_simpson_3_8
from calculos.linealizacioncrecimiento import metodo_linealizacion_crecimiento
from calculos.interpolacionlagrange import lagrange
from calculos.regresionmultilineal import calcular_regresion
from calculos.simpson1_3 import simpson1_3
from calculos.falsaposicion import calcular_falsa_posicion
from calculos.regresion_polinomial import regresion_polinomial
from calculos.trapecio import metodo_trapecio
from calculos.regresion_saturado import metodo_regresion_crecimiento_saturado
from calculos.runge_kutta_4 import runge_kutta_4, validar_ecuaciones
from calculos.linealizacionexponencial import exponencial
from calculos.linealizacionpotencial import potencial
from calculos.gauss_jordan import validar_matriz, calcular_gauss_jordan
from calculos.gauss_simple import validar_matriz_aumentada, gauss_simple, convertir_matriz_a_html
from calculos.derivacionatras import calcular_derivacion_atras
from calculos.derivacionadelante import calcular_derivacion_adelante
from calculos.derivacioncentral import calcular_derivacion_central
from calculos.metodoeuler import metodo_euler
from calculos.integracionmultiple import integracionmultiple
from calculos.biseccion import biseccion, f, convertir_resultados_a_html
from calculos.eliminacion_gaussiana import validar_matriz, eliminacion_gaussiana
from calculos.newton import newton_raphson
from calculos.interpolacion_matricial import interpolacion_por_matrices
from calculos.interpolacion_newton import interpolacion_newton




app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


##______________________________________________
##PAGINA DE INICIO
@app.route('/')
def home():
    rutas_get = [
        {
            "categoria": "Series",
            "metodos": [
                {"nombre": "Serie de Taylor", "url": "/serie-taylor"},
                {"nombre": "Serie de McLaren", "url": "/serie-mclaurin"},
            ]
        },
        {
            "categoria": "Métodos Numéricos",
            "metodos": [
                {"nombre": "Matriz Inversa", "url": "/matriz_inversa"},
                {"nombre": "Metodo Punto Fijo", "url": "/metodo-punto-fijo"},
                {"nombre": "Metodo Simpson 3/8", "url": "/metodo-simpson-3_8"},
                {"nombre": "Metodo Gauss-Jordan", "url": "/gauss_jordan"},
                {"nombre": "Metodo Gauss Simple", "url": "/gauss_simple"},
                {"nombre": "Método Eliminación Gaussiana", "url": "/eliminacion_gaussiana"},
            ]
        },
        {
            "categoria": "Linealizacion",
            "metodos": [
                {"nombre": "Linealizacion a razon de crecimiento", "url":"/linealizacion-a-razon-crecimiento"},
                {"nombre": "Linealizacion exponencial", "url":"/exponencial"},
                {"nombre": "Linealizacion potencial", "url":"/potencial"},
            ]
        },
        {
            "categoria": "Regresiones",
            "metodos": [
                {"nombre": "Regresion por crecimiento de saturación", "url": "/regresion-crecimiento-saturado"},
                {"nombre": "Regresion multilineal", "url": "/regresion-multilineal"},
                {"nombre": "Regresión Polinomial", "url": "/regresion-polinomial"},
            ]
        },
        {
            "categoria": "Interpolaciones",
            "metodos": [
                {"nombre": "Interpolación por matrices", "url": "/interpolacion_matricial"},
                {"nombre": "Interpolación por Newton", "url": "/interpolacion_newton"},
                
            ]
        },

        {
            "categoria": "Integración",
            "metodos": [
                {"nombre": "Integración por Simpson 1_3", "url": "/simpson1_3"},
                {"nombre": "Integración por Método de Trapecio", "url": "/metodo-trapecio"},
                {"nombre": "Integración múltiple", "url": "/integracionmultiple"},
            ]
        },
        {
            "categoria": "Diferenciacion",
            "metodos": [
                {"nombre": "Diferenciacion numerica hacia atras", "url":"/derivada-atras"},
                {"nombre": "Diferenciacion numerica hacia adelante", "url":"/derivada-adelante"},
                {"nombre": "Diferenciacion numerica central", "url":"/derivada-central"},
                {"nombre": "Metodo de biseccion", "url":"/biseccion"},
                {"nombre": "Metodo de Newton", "url":"/newton"},
            ]
        },
        {
            "categoria": "Ecuaciones Diferenciales",
            "metodos": [
                {"nombre": "E.c Diferenciales Runge Kutta Orden 4", "url": "/runge-kutta"},
                {"nombre": "E.c Diferenciales Metodo de Euler", "url": "/metodo-euler"},
            ]
        },
    ]
    return render_template('principal/inicio.html', rutas=rutas_get)


##_____________________________________________


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

## METODO DE REGRESIÓN POLINOMIAL

##______________________________________________
@app.route('/regresion-polinomial', methods=['GET'])
def regresion_polinomial_get():
    return render_template('regresion/RegresionPolinomial.html')

@app.route('/regresion-polinomial', methods=['POST'])
def regresion_polinomial_post():
    try:
        # Obtener datos del cliente
        datos = request.get_json()
        x_values = list(map(float, datos['x_values']))
        y_values = list(map(float, datos['y_values']))
        grado = int(datos['grado'])

        # Calcular la regresión polinomial
        resultado = regresion_polinomial(x_values, y_values, grado)

        # Responder con los resultados
        return jsonify(resultado)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor. '}), 500

##______________________________________________


## METODO DE INTEGRACION POR TRAPECIO

##______________________________________________
@app.route('/metodo-trapecio', methods=['GET'])
def metodo_trapecio_get():
    return render_template('integracion/Trapecio.html')

@app.route('/metodo-trapecio', methods=['POST'])
def metodo_trapecio_post():
    try:
        datos = request.json
        funcion_str = datos.get('funcion')
        valor_a = float(datos.get('valor_a'))
        valor_b = float(datos.get('valor_b'))
        subintervalos = int(datos.get('subintervalos'))


        if funcion_str is None or valor_a is None or valor_b is None or subintervalos is None:
            return jsonify({'error': 'Todos los campos son necesarios.'}), 400

        # Calcular la regresión polinomial
        resultado = metodo_trapecio(funcion_str, valor_a, valor_b, subintervalos)

        # Responder con los resultados
        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

##______________________________________________


##METODO DE RUNGE KUTTA ORDEN 4

##______________________________________________

@app.route('/runge-kutta', methods=['GET'])
def runge_kutta_get():
    return render_template('ecuaciones_diferenciales/runge_kutta.html')

@app.route('/runge-kutta', methods=['POST'])
def runge_kutta_post():
    try:
        datos = request.json
        ecuaciones = datos.get('ecuaciones', [])
        variables = datos.get('variables', [])
        x0 = float(datos.get('x0'))
        valores_iniciales = [float(v) for v in datos.get('valores_iniciales', [])]
        h = float(datos.get('h'))
        n = int(datos.get('n'))


        print("Valores recibidos")
        print(ecuaciones)
        print(variables)
        print(x0)
        print(valores_iniciales)
        print(h)
        print(n)

        if not ecuaciones or not variables or len(ecuaciones) != len(variables):
            return jsonify({'error': 'Debe haber tantas ecuaciones como variables dependientes.'}), 400
        if len(valores_iniciales) != len(variables):
            return jsonify({'error': 'Debe proporcionar valores iniciales para todas las variables dependientes.'}), 400
        if h <= 0 or n <= x0:
            return jsonify({'error': 'El tamaño del paso debe ser positivo y x_n > x_0.'}), 400

        # Validar ecuaciones
        ecuaciones_validadas = validar_ecuaciones(ecuaciones, variables)

        print("Ecuaciones validadas: ")
        print(ecuaciones_validadas)

        # Calcular método de Runge-Kutta
        resultado = runge_kutta_4(ecuaciones_validadas, variables, x0, valores_iniciales, h, n)

        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'error': "Error en el metodo post (app.py)" + str(e)}), 400

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

    ##matriz_np, error = validar_matriz(matriz)
    ##if error:
    ##    return jsonify(matriz_np), error

    resultado, error = calcular_inversa(matriz)
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
def metodo_punto_fijo():
    try:
        data = request.get_json()
        funcion_str = data['funcion']
        x0 = float(data['x0'])
        tolerancia = float(data['tolerancia'])
        iteraciones_max = int(data['iteraciones'])
        resultado, error = metodo_punto_fijo_calculo(funcion_str, x0, tolerancia, iteraciones_max)
        
        if error > tolerancia:
            return jsonify({"error": "No se alcanzó la convergencia en el número máximo de iteraciones."}), 400
        buffer = calcular_y_graficar(funcion_str, x0, tolerancia, iteraciones_max)
        return send_file(buffer, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 400
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

        return jsonify({
            "resultado_tabla_x": resultado["datos_lin_x"],
            "resultado_tabla_y": resultado["datos_lin_y"],
        })

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"})

##______________________________________________
##DIFERENCIACION HACIA ATRAS
@app.route('/derivada-atras', methods=['GET'])
def calcular_derivada_atras_get():
    return render_template('Diferenciacion/HaciaAtras.html')
@app.route('/derivada-atras', methods=['POST'])
def calcular_derivada_atras_post():
    datos = request.json
    valores = datos.get('datos')
    tipo = datos.get('tipo')
    
    try:
        resultado = calcular_derivacion_atras(valores, tipo)
        return jsonify(
            {'resultado_tabla': resultado["tabla"]}
        )
    except Exception as e:
        return jsonify({'error': f'Error al calcular: {str(e)}'}), 500


##______________________________________________
##DIFERENCIACION HACIA ADELANTE
@app.route('/derivada-adelante', methods=['GET'])
def calcular_derivada_adelante_get():
    return render_template('Diferenciacion/HaciaAdelante.html')
@app.route('/derivada-adelante', methods=['POST'])
def calcular_derivada_adelante_post():
    datos = request.json
    valores = datos.get('datos')
    tipo = datos.get('tipo')
    
    try:
        resultado = calcular_derivacion_adelante(valores, tipo)
        return jsonify(
            {'resultado_tabla': resultado["tabla"]}
        )
    except Exception as e:
        return jsonify({'error': f'Error al calcular: {str(e)}'}), 500


##______________________________________________
##DIFERENCIACION CENTRAL
@app.route('/derivada-central', methods=['GET'])
def calcular_derivada_central_get():
    return render_template('Diferenciacion/Central.html')
@app.route('/derivada-central', methods=['POST'])
def calcular_derivada_central_post():
    datos = request.json
    valores = datos.get('datos')
    tipo = datos.get('tipo')
    
    try:
        resultado = calcular_derivacion_central(valores, tipo)
        return jsonify(
            {'resultado_tabla': resultado["tabla"]}
        )
    except Exception as e:
        return jsonify({'error': f'Error al calcular: {str(e)}'}), 500


##______________________________________________
##REGRESION POR CRECIMIENTO DE SATURACION
@app.route('/regresion-crecimiento-saturado', methods=['GET'])
def calcular_regresion_saturado_get():
    return render_template('Regresion/RegresionSaturado.html')
@app.route('/regresion-crecimiento-saturado', methods=['POST'])
def calcular_regresion_saturado_post():
    try:
        data = request.get_json()
        datos = data.get('valores')

        datos_lin = metodo_linealizacion_crecimiento(datos)
        resultado = metodo_regresion_crecimiento_saturado(datos_lin, datos)
        return jsonify({
            "resultado_funcion": resultado["funcion"],
            "resultado_tabla_ycal" : resultado["tabla_ycal"],
            "resultado_tabla_y" : resultado["tabla_y"],
            "resultado_tabla_x" : resultado["tabla_x"],
            "resultado_grafico" : resultado["grafico"]
        })

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"})

##______________________________________________
##METODO DE EULER PARA EDO
@app.route('/metodo-euler', methods=['GET'])
def calcular_metodo_euler_get():
    return render_template('ecuaciones_diferenciales/Euler.html')
@app.route('/metodo-euler', methods=['POST'])
def calcular_metodo_euler_post():
    try:
        data = request.get_json()
        datos = data.get('datos')

        resultado = metodo_euler(datos)
        
        return jsonify({
            "resultado_valor": resultado["numero"],
            "resultado_valor_n" : resultado["n"]
        })

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error: {str(e)}"})


##Hasta aqui terminan mis metodos (Jeycson)
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

##[

    ##METODOS DE JUAN

##]

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
        return serie
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la interpolación de Lagrange: {str(e)}'}), 500

##______________________________________________

##______________________________________________
        
#METODO DE LINEALIZACIÓN EXPONENCIAL  

@app.route('/exponencial', methods=['GET'])
def calcular_exponencial_get():
    return render_template('Linealizacion/Exponencial.html')
@app.route('/exponencial', methods=['POST'])
def calcular_exponencial_post():
    datos = request.json
    puntos = datos.get('puntos')

    if not puntos:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        expo = exponencial(puntos)
        return expo
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la función por linealización exponencial: {str(e)}'}), 500

##______________________________________________

##[


##______________________________________________
        
#METODO DE LINEALIZACIÓN POTENCIAL  

@app.route('/potencial', methods=['GET'])
def calcular_potencial_get():
    return render_template('Linealizacion/Potencial.html')
@app.route('/potencial', methods=['POST'])
def calcular_potencial_post():
    datos = request.json
    puntos = datos.get('puntos')

    if not puntos:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        pot = potencial(puntos)
        return pot
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la función por linealización potencial: {str(e)}'}), 500

##______________________________________________
        
#METODO DE INTEGRACIÓN MÚLTIPLE 

@app.route('/integracionmultiple', methods=['GET'])
def calcular_integracionmultiple_get():
    return render_template('Integracion/integracionmultiple.html')
@app.route('/integracionmultiple', methods=['POST'])
def calcular_integracionmultiple_post():
    datos = request.json
    funcion = datos.get('funcion')
    x0 = datos.get('limites_inferiores')
    xn = datos.get('limites_superiores')
    numero_n = datos.get('n')
    variables = datos.get('variables')
    cantidad_integraciones = datos.get('cant')

    if not funcion or not x0  or not xn or not variables or numero_n is None or cantidad_integraciones is None:
        return jsonify({'error': 'Todos los campos son necesarios.'}), 400

    try:
        im = integracionmultiple(funcion, x0, xn, variables, numero_n, cantidad_integraciones)
        return jsonify({'funcion': str(im)})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al calcular la integración múltiple: {str(e)}'}), 500

##______________________________________________

##______________________________________________



##[

    ##METODOS DE GERSON

##]

##_________Eliminación Gaussiana______________

@app.route('/eliminacion_gaussiana', methods=['GET'])
def calcular_eliminacion_gaussiana_get():
    return render_template('Matrices/EliminacionGaussiana.html')

@app.route('/eliminacion_gaussiana', methods=['POST'])
def calcular_eliminacion_gaussiana_post():
    datos = request.json
    matriz = datos.get('matrix') 

    matriz_np, error = validar_matriz(matriz)
    if error:
        return jsonify(matriz_np), error

    resultado, error = eliminacion_gaussiana(matriz_np)
    if error:
        return jsonify(resultado), error

    return jsonify(resultado)



##_________Interpolación por matrices______________
@app.route('/interpolacion_matricial', methods=['GET'])
def interpolacion_matrices_get():
    """Renderiza la página HTML donde el usuario ingresa los valores."""
    return render_template('interpolacion/SistemasMatriz.html')

@app.route('/interpolacion_matricial', methods=['POST'])
def interpolacion_matrices_post():
    """Recibe los datos del formulario y realiza la interpolación."""
    datos = request.json
    x_puntos = datos.get('x')  # Lista de valores X
    y_puntos = datos.get('y')  # Lista de valores Y
    x_eval = datos.get('evaluar')  # Valor en X a evaluar

    # Validar y ejecutar interpolación
    resultado, error = interpolacion_por_matrices(x_puntos, y_puntos, x_eval)
    if error:
        return jsonify(resultado), error

    return jsonify(resultado)


##_________Interpolación Newton______________

@app.route('/interpolacion_newton', methods=['GET'])
def calcular_interpolacionNewton_get():
    return render_template('interpolacion/Newton.html')

@app.route('/interpolacion_newton', methods=['POST'])
def calcular_interpolacionNewton_post():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    x_eval = data.get('evaluar')

    resultado, error = interpolacion_newton(x, y, x_eval)
    
    if error:
        return jsonify(resultado), error
    
    return jsonify(resultado)



##[

    ##METODOS DE wachomin

##]

##______________________________________________

#______________Metodo de gauss jordan__________________

@app.route('/gauss_jordan', methods=['GET'])
def calcular_gauss_jordan_get():
    return render_template('Matrices/GaussJordan.html')

@app.route('/gauss_jordan', methods=['POST'])
def calcular_gauss_jordan_post():
    datos = request.json
    matriz = datos.get('matrix') 

    matriz_np, error = validar_matriz(matriz)
    if error:
        return jsonify(matriz_np), error

    resultado, error = calcular_gauss_jordan(matriz_np)
    if error:
        return jsonify(resultado), error

    return jsonify(resultado)
#_____________________________________________________
#METODO DE GAUSS SIMPLE

@app.route('/gauss_simple', methods=['GET'])
def calcular_gauss_simple_get():
    return render_template('Matrices/GaussSimple.html')

@app.route('/gauss_simple', methods=['POST'])
def calcular_gauss_simple_post():
    datos = request.json
    matriz = datos.get('matrix')

    matriz_np, error = validar_matriz_aumentada(matriz)
    if error:
        return jsonify(matriz_np), error

    resultado, error = gauss_simple(matriz_np)
    if error:
        return jsonify(resultado), error

    return jsonify(resultado)


#_________________________________________________________


#_______________METODO DE BISECCION________________________
@app.route('/biseccion', methods=['GET'])
def biseccion_get():
    return render_template('metodos_raices/Biseccion.html')

@app.route('/biseccion', methods=['POST'])
def biseccion_post():
    datos = request.json
    xl = datos['xl']
    xu = datos['xu']
    tol = datos['tol']
    max_iter = datos['max_iter']
    g = datos['g']
    m = datos['m']
    t = datos['t']
    v = datos['v']

    try:
        resultado = biseccion(f, xl, xu, tol, max_iter, g, m, t, v)
        resultado['tabla'] = convertir_resultados_a_html(resultado['resultados'])
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)})


#------------------------------ NEWTON -----------------------------------------------#

@app.route("/newton", methods=["GET", "POST"])
def newton():
    if request.method == "GET":
        return render_template("metodos_raices/newton.html")
    elif request.method == "POST":
        datos = request.json
        x0 = float(datos["x0"])
        tol = float(datos["tol"])
        max_iter = int(datos["max_iter"])

        resultado = newton_raphson(x0, tol, max_iter)
        return jsonify(resultado)
#-----------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True,  host='127.0.0.1', port=5000)
