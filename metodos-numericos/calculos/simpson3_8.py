import math

def calcular_simpson_3_8(funcion_str, limite_inferior, limite_superior, subintervalos):
    try:
        if subintervalos % 3 != 0:
            raise ValueError("El número de subintervalos debe ser múltiplo de 3.")
        
        def funcion(x):
            return eval(funcion_str)
        
        h = (limite_superior - limite_inferior) / subintervalos
        resultado = funcion(limite_inferior) + funcion(limite_superior)

        for i in range(1, subintervalos):
            x = limite_inferior + i * h
            if i % 3 == 0:
                resultado += 2 * funcion(x)
            else:
                resultado += 3 * funcion(x)

        resultado *= 3 * h / 8

        return resultado

    except Exception as e:
        raise ValueError(f"Error en el cálculo: {str(e)}")
