import math
import matplotlib.pyplot as plt
import io
import base64

# Definir la función f(h)
def f(h):
    return 3 * math.pi * h**2 - (math.pi * h**3) / 3 - 30

# Definir la derivada de la función f'(h)
def f_prime(h):
    return 6 * math.pi * h - math.pi * h**2

# Método de Newton-Raphson
def newton_raphson(x0, tol, max_iter):
    iteraciones = []
    errores = []
    valores_x = []

    for i in range(max_iter):
        fx = f(x0)
        fpx = f_prime(x0)
        
        if fpx == 0:
            return {"error": "Derivada cero. No se puede continuar."}
        
        xr = x0 - fx / fpx
        error = abs((xr - x0) / xr)

        iteraciones.append({
            "iteracion": i + 1,
            "x0": x0,
            "xr": xr,
            "error": error
        })
        valores_x.append(xr)
        errores.append(error)
        
        if error < tol:
            break
        
        x0 = xr

    return {
        "raiz": xr,
        "iteraciones": iteraciones,
        "grafica": generar_grafica(valores_x, errores)
    }

# Función para generar la gráfica
def generar_grafica(valores_x, errores):
    plt.figure()
    plt.plot(range(1, len(valores_x) + 1), valores_x, marker="o", label="Valor de xr")
    plt.xlabel("Iteraciones")
    plt.ylabel("Valor de xr")
    plt.title("Método de Newton-Raphson")
    plt.legend()
    plt.grid()

    # Guardar la imagen en base64
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    grafica_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
    plt.close()
    
    return grafica_base64
