import numpy as np
import matplotlib.pyplot as plt
import os
import uuid  # Para nombres únicos en las imágenes

def validar_datos(x, y, x_eval):
    """Valida los datos de entrada para la interpolación."""
    if len(x) != len(y):
        return {'error': 'Las listas de X e Y deben tener la misma longitud.'}, 400
    if len(x) < 2 or len(x) > 5:
        return {'error': 'Se requiere al menos 2 puntos y un máximo de 5 para la interpolación.'}, 400
    if len(set(x)) != len(x):
        return {'error': 'Los valores de X no pueden repetirse.'}, 400
    return None

def diferencias_divididas(x, y):
    """Calcula los coeficientes del polinomio de Newton con diferencias divididas."""
    n = len(x)
    coef = np.copy(y).astype(float)

    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])
    
    return coef  # Coeficientes del polinomio

def polinomio_newton(x, coef, x_eval):
    """Evalúa el polinomio interpolador de Newton en x_eval."""
    n = len(coef)
    resultado = coef[-1]
    
    for i in range(n - 2, -1, -1):
        resultado = resultado * (x_eval - x[i]) + coef[i]
    
    return resultado

def construir_polinomio(x, coef):
    """Devuelve el polinomio interpolador en formato string."""
    n = len(coef)
    terminos = [f"{coef[0]:.4f}"]

    for i in range(1, n):
        factores = "".join(f"(x - {x[j]})" for j in range(i))
        if coef[i] != 0:
            terminos.append(f"{coef[i]:.4f}*{factores}")

    return "f(x) = " + " + ".join(terminos).replace("x^1", "x")

def generar_grafica_newton(x, y, coef, x_eval, f_x_eval):
    """Genera la gráfica del polinomio de Newton y la guarda con un nombre único."""
    x_range = np.linspace(min(x) - 1, max(x) + 1, 1000)
    y_range = [polinomio_newton(x, coef, xi) for xi in x_range]

    plt.figure(figsize=(8, 6))
    plt.plot(x_range, y_range, label="Polinomio Interpolador", color='blue')
    plt.scatter(x, y, color='red', zorder=5, label="Puntos dados")
    plt.scatter(x_eval, f_x_eval, color='green', zorder=10, label=f'Punto Evaluado ({x_eval}, {f_x_eval:.4f})')

    plt.title('Interpolación de Newton')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    imagen_name = f"grafica_newton_{str(uuid.uuid4())}.png"
    image_path = os.path.join('static', imagen_name)

    plt.savefig(image_path)
    plt.close()

    return image_path

def interpolacion_newton(x, y, x_eval):
    """Calcula la interpolación de Newton y devuelve el polinomio, evaluación y gráfica."""
    try:
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        x_eval = float(x_eval)

        # Validar datos
        error = validar_datos(x, y, x_eval)
        if error:
            return error

        # Calcular coeficientes
        coef = diferencias_divididas(x, y)

        # Construir polinomio en string
        polinomio_str = construir_polinomio(x, coef)

        # Evaluar en x_eval
        f_x_eval = polinomio_newton(x, coef, x_eval)

        # Generar gráfica
        imagen_path = generar_grafica_newton(x, y, coef, x_eval, f_x_eval)

        # Convertir resultado a HTML
        resultado_html = convertir_resultado_a_html(polinomio_str, x_eval, f_x_eval, imagen_path)
        return {'resultado': resultado_html}, None

    except Exception as e:
        return {'error': f'Error en la interpolación: {str(e)}'}, 500

def convertir_resultado_a_html(polinomio, x_eval, resultado, imagen_path):
    """Convierte el polinomio, la evaluación y la imagen en HTML."""
    html = f"""
    <h2>Polinomio Interpolador de Newton:</h2>
    <p>{polinomio.replace("+ -", "- ")}</p>
    <h2>Evaluación en x = {x_eval}:</h2>
    <p>f({x_eval}) = {resultado:.4f}</p>
    <h2>Gráfica:</h2>
    <img src="{imagen_path}" alt="Gráfica de la Interpolación de Newton">
    """
    return html
