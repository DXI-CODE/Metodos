import math

def metodo_linealizacion_crecimiento(datos):
    try:
        x = datos['x']
        y = datos['y']
        
        lin_x = []
        lin_y = []
        for x, y in zip(x, y):
            if x == 0:
                lin_x.append("Null")
            elif y == 0:
                lin_y.append("Null")
            else:
                lin_x.append(1/x)
                lin_y.append(1/y)

        return {"datos_lin_x": lin_x,
                "datos_lin_y": lin_y}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
