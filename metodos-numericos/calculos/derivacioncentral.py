import numpy as np
import sympy as sp

def primera(x2m, x1m, x1p, x2p, h):
    return ((-1 * x2p + 8 * x1p - 8 * x1m + x2m) / (12 * h))
def segunda(x2m, x1m, x0, x1p, x2p, h):
    return ((-1 * x2p + 16 * x1p - 30 * x0 + 16 * x1m - x2m)/(12 * (h ** 2)))
def tercera(x3m, x2m, x1m, x1p, x2p, x3p, h):
    return ((-1 * x3p + 8 * x2p - 13 * x1p + 13 * x1m - 8 * x2m + x3m)/(8 * (h ** 3)))
def cuarta(x3m, x2m, x1m, x0, x1p, x2p, x3p, h):
    return ((-1 * x3p + 12 * x2p + 39 * x1p + 56 * x0 - 39 * x1m + 12 * x2m + x3m)/(6 * (h ** 4)))

def calcular_derivacion_central(datos, tipo):
    res = {}
    
    if tipo == "Funcion":
        funcion = datos["funcion"]
        valor = datos["valor"]
        paso = datos["paso"]
        derivadas = datos["derivadas"]
        
        if not funcion or not paso or not valor:
            return {"error": "Faltan datos obligatorios: función o paso."}
        
        valor = float(valor)
        paso = float(paso)
        
        x = sp.symbols('x')
        function = sp.lambdify(x, funcion, 'numpy')
        y = []    
        temp = valor

        try:
            y.append(float(function(temp)))
        except Exception as e:
            return {"error": f"Error al evaluar la función: {e}"}

        for _ in range(3):
            temp -= paso 
            try:
                y.insert(0, float(function(temp)))
            except Exception as e:
                return {"error": f"Error al evaluar la función: {e}"}

        temp = valor + paso 
        for _ in range(3):
            try:
                y.append(float(function(temp))) 
            except Exception as e:
                return {"error": f"Error al evaluar la función: {e}"}
            temp += paso
        #y[0] = y[i-3], y[1] = y[i-2], y[2] = y[i-1], y[3] = y[i], y[4] = y[i+1], y[5] = y[i+2], y[6] = y[i+3]
        for derivada in derivadas:
            if derivada == "primera":
                res["primera"] = primera(y[1], y[2], y[4], y[5], paso)
            if derivada == "segunda":
                res["segunda"] = segunda(y[1], y[2], y[3], y[4], y[5], paso)
            if derivada == "tercera":
                res["tercera"] = tercera(y[0], y[1], y[2], y[4], y[5], y[6], paso)
            if derivada == "cuarta":
                res["cuarta"] = cuarta(y[0], y[1], y[2], y[3], y[4], y[5], y[6], paso)
    elif tipo == "Datos":
        x = datos["xValues"]
        y = datos["yValues"]
        valor = datos["valorDatos"]
        derivadas = datos["derivadas"]
        x = [float(i) for i in x]
        y = [float(i) for i in y]
        pares_ordenados = sorted(zip(x, y), key=lambda p: p[0])
        x, y = zip(*pares_ordenados)
        if not x or not y:
            return {"error": "Faltan datos obligatorios: x o y."}
        if not valor is None:
            valor = float(valor)
            if len(x) < 5:
                return {"error": "Se debe ingresar minimo 5 datos."}
            paso = 0.1
            if x[0] < x[-1]: 
                if len(x) == 5 and x[2] != valor:
                    return {"error": "El dato del centro tiene que ser el valor a calcular."}
                if not (x[0] <= valor <= x[-1]):
                    return {"error": "El valor está fuera del rango."}
                paso = x[1] - x[0]
            
            indice_cercano = min(range(len(x)), key=lambda i: abs(x[i] - valor))
            
            for derivada in derivadas:
                if derivada == "primera":
                    if indice_cercano - 2 >= 0 and indice_cercano + 2 < len(x):  # Verificamos 2 valores antes y 2 valores después
                        aux = [primera(
                            y[indice_cercano - 2], y[indice_cercano - 1], y[indice_cercano + 1], y[indice_cercano + 2], paso
                        )]
                        res["primera"] = aux
                    else:
                        return {"error": "No hay suficientes datos para calcular la primera derivada"}


                if derivada == "segunda":
                    if indice_cercano - 2 >= 0 and indice_cercano + 2 < len(x):  # Verificamos 2 valores antes y 2 valores después
                        aux = [segunda(
                            y[indice_cercano - 2], 
                            y[indice_cercano - 1],
                            y[indice_cercano], 
                            y[indice_cercano + 1],
                            y[indice_cercano + 2],
                            paso
                        )]
                        res["segunda"] = aux
                    else:
                        return {"error": "No hay suficientes datos para calcular la segunda derivada"}

                if derivada == "tercera":
                    if indice_cercano - 3 >= 0 and indice_cercano + 3 < len(x):  # Verificamos 3 valores antes y 3 valores después
                        aux = [tercera(
                            y[indice_cercano - 3],
                            y[indice_cercano - 2], 
                            y[indice_cercano - 1],
                            y[indice_cercano + 1],
                            y[indice_cercano + 2],
                            y[indice_cercano + 3],
                            paso
                        )]
                        res["tercera"] = aux
                    else:
                        return {"error": "No hay suficientes datos para calcular la tercera derivada"}

                if derivada == "cuarta":
                    if indice_cercano - 3 >= 0 and indice_cercano + 3 < len(x):  # Verificamos 3 valores antes y 3 valores después
                        aux = [cuarta(
                            y[indice_cercano - 3],
                            y[indice_cercano - 2], 
                            y[indice_cercano - 1],
                            y[indice_cercano],
                            y[indice_cercano + 1],
                            y[indice_cercano + 2],
                            y[indice_cercano + 3],
                            paso
                        )]
                        res["cuarta"] = aux
                    else:
                        return {"error": "No hay suficientes datos para calcular la cuarta derivada"}
        else:
            valores_derivados = []
            paso = 0.1
            for derivada in derivadas:
                if derivada == "primera":
                    if len(x) < 5:
                        return{"error": "No hay suficientes datos para calcular la primera derivada"}
                    paso = x[1] - x[0]
                    valores_derivados = [
                        primera(y[i-2], y[i-1], y[i+1], y[i+2], paso)
                        for i in range(2, len(y) - 2)  # El rango asegura 2 valores antes y después
                    ]

                    arreglo_final = [None, None] + valores_derivados + [None, None]
                    res["primera"] = arreglo_final

                    #los primero y ultimos dos valores no se calculan y en el front deberian mostrar null
                        
                if derivada == "segunda":
                    if len(x) < 5:
                        return{"error": "No hay suficientes datos para calcular la segunda derivada"}
                    valores_derivados = [
                        segunda(y[i-2], y[i-1], y[i], y[i+1], y[i+2], paso)
                        for i in range(2, len(y) - 2)  # El rango asegura 2 valores antes y después
                    ]

                    arreglo_final = [None, None] + valores_derivados + [None, None]
                    res["segunda"] = arreglo_final

                if derivada == "tercera":
                    if len(x) < 7:
                        return{"error": "No hay suficientes datos para calcular la tercera derivada"}
                    paso = x[1] - x[0]
                    valores_derivados = [
                        tercera(y[i-3], y[i-2], y[i-1], y[i+1], y[i+2], y[i+3], paso)
                        for i in range(3, len(y) - 3)  # Aseguramos que haya 3 valores antes y 3 después
                    ]

                    arreglo_final = [None, None, None] + valores_derivados + [None, None, None]
                    res["tercera"] = arreglo_final

                if derivada == "cuarta":
                    if len(x) < 7:
                        return{"error": "No hay suficientes datos para calcular la cuarta derivada"}
                    paso = x[1] - x[0]
                    valores_derivados = [
                        cuarta(y[i-3], y[i-2], y[i-1], y[i], y[i+1], y[i+2], y[i+3], paso)
                        for i in range(3, len(y) - 3)  # Aseguramos que haya 3 valores antes y 3 después
                    ]

                    arreglo_final = [None, None, None] + valores_derivados + [None, None, None]
                    res["cuarta"] = arreglo_final

    return {
        "tabla": res,
    }