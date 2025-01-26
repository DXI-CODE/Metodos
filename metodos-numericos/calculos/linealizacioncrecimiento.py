def metodo_linealizacion_crecimiento(datos):
    try:
        # Verificar si 'datos' es None o no tiene las claves necesarias
        if not datos or 'x' not in datos or 'y' not in datos:
            return {"error": "Los datos proporcionados no son válidos. Asegúrate de incluir 'x' y 'y'."}
        
        x_vals = datos['x']
        y_vals = datos['y']
        
        # Verificar si x_vals o y_vals son None
        if x_vals is None or y_vals is None:
            return {"error": "'x' o 'y' tienen un valor None, lo cual no es válido."}
        
        lin_x = []
        lin_y = []
        for x_val, y_val in zip(x_vals, y_vals):
            if x_val == 0:
                lin_x.append("Null")
            elif y_val == 0:
                lin_y.append("Null")
            else:
                lin_x.append(1/x_val)
                lin_y.append(1/y_val)

        return {"datos_lin_x": lin_x,
                "datos_lin_y": lin_y}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
