import math
import matplotlib.pyplot as plt
import io
import base64

# Función original
def f(h):
    return 3 * math.pi * h**2 - (math.pi * h**3) / 3 - 30

# Derivada de la función
def f_prime(h):
    return 6 * math.pi * h - math.pi * h**2

# Método de Newton-Raphson
def newton_raphson(x0, tol, max_iter):
    iteraciones = []
    x_values = []

    for i in range(max_iter):
        fx = f(x0)
        fpx = f_prime(x0)

        if fpx == 0:
            return {"error": "Derivada cero. No se puede continuar."}

        xr = x0 - fx / fpx
        error = abs((xr - x0) / xr)

        iteraciones.append({
            "iteracion": i + 1,
            "x0": round(x0, 6),
            "xr": round(xr, 6),
            "error": round(error, 6)
        })

        x_values.append(xr)

        if error < tol:
            break

        x0 = xr

    grafica_url = generar_grafica(x_values)

    return {
        "raiz": round(xr, 6),
        "iteraciones": iteraciones,
        "grafica": grafica_url
    }

# Función para generar la gráfica de convergencia
def generar_grafica(x_values):
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(x_values) + 1), x_values, marker='o', linestyle='-', color='b')
    plt.xlabel('Iteración')
    plt.ylabel('Valor de xr')
    plt.title('Convergencia del Método de Newton-Raphson')
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.getvalue()).decode()
