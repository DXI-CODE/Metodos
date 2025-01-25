import math

def metodo_punto_fijo(funcion_str, x0, tolerancia, iteraciones_max):
    try:
        def g(x):
            return eval(funcion_str, {"x": x, "math": math})

        x_prev = x0
        for i in range(iteraciones_max):
            x_next = g(x_prev)
            error_aproximado = abs(x_next - x_prev)

            if error_aproximado < tolerancia:
                return {
                    "raiz": x_next,
                    "iteraciones": i + 1,
                    "error_aproximado": error_aproximado
                }

            x_prev = x_next

        return {
            "error": "No se alcanzó la tolerancia deseada dentro del número máximo de iteraciones.",
            "iteraciones": iteraciones_max
        }

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
