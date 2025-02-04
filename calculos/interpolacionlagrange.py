import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math as math

def lagrange(puntos, grado, x):
    
    if(grado < 1 or grado > 4):
        raise ValueError('Elige un grado entre 1 y 4.')
    
    puntos_ord = sorted(puntos)

    x_vals = np.array([p[0] for p in puntos_ord])
    y_vals = np.array([p[1] for p in puntos_ord])

    if len(set(x_vals)) != len(x_vals):
        raise ValueError('Los valores de X deben ser únicos.')
    
    if grado >= len(x_vals):
        raise ValueError(f'Debe haber al menos {grado + 1} valores para la interpolación.')
    
    sum = 0
    for i in range(grado + 1):
        product = y_vals[i]
        for j in range(grado + 1):
            if i != j:
                product *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])
        sum += product

    try:
        
        fig, ax = plt.subplots()
        ax.plot([fila[0] for fila in puntos_ord], [fila[1] for fila in puntos_ord], marker='o', linewidth=0.2, label="Puntos originales")
        ax.plot(x, sum, marker='o' ,label=f'Resultado obtenido con interpolación de grado {grado}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.set_title('Ecuación obtenida')

        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        grafico_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close(fig)
    except Exception as e:
        print(f"Error al generar la gráfica: {e}")
        grafico_base64 = None
        return {'error': e}

    return {'grafico_base64': grafico_base64, 'funcion': sum}