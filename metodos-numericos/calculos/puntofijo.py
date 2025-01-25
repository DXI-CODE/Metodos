import math

def metodo_punto_fijo(funcion_str, x0, tolerancia, iteraciones_max):
    try:
        def g(x):
            return eval(funcion_str, {"x": x, "math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan})

        x_prev = x0
        iteraciones_data = []  
        for i in range(iteraciones_max):
            x_next = g(x_prev)
            iteraciones_data.append(x_next) 
            error_aproximado = abs(x_next - x_prev)
            if error_aproximado < tolerancia:
                return {
                    "raiz": x_next,
                    "iteraciones": i + 1,
                    "error_aproximado": error_aproximado,
                    "iteraciones_data": iteraciones_data  
                }

            x_prev = x_next
        
        return {
            "error": "No se alcanzó la tolerancia deseada dentro del número máximo de iteraciones.",
            "iteraciones": iteraciones_max,
            "iteraciones_data": iteraciones_data
        }

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
