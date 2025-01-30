import numpy as np
import matplotlib.pyplot as plt
import os

def validar_datos(x, y, x_eval):
    """Valida los datos de entrada para la interpolación."""
    if len(x) != len(y):
        return {'error': 'Las listas de X e Y deben tener la misma longitud.'}, 400
    if len(x) < 2 or len(x) > 5:
        return {'error': 'Se requiere al menos 2 puntos y un máximo de 5 para la interpolación.'}, 400
    if len(set(x)) != len(x):
        return {'error': 'Los valores de X no pueden repetirse.'}, 400
    return None

def interpolacion_por_matrices(x, y, x_eval):
    """Realiza la interpolación utilizando la matriz de Vandermonde y genera una gráfica."""
    try:
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        x_eval = float(x_eval)

        # Validar los datos
        error = validar_datos(x, y, x_eval)
        if error:
            return error

        # Construcción de la matriz de Vandermonde
        A = np.vander(x, increasing=True)
        
        # Resolver el sistema para obtener coeficientes del polinomio
        coeficientes = np.linalg.solve(A, y)

        # Formatear el polinomio como string
        polinomio_str = "f(x) = " + " + ".join(
            f"{coef:.4f} * x^{i}" if i > 0 else f"{coef:.4f}"
            for i, coef in enumerate(coeficientes) if coef != 0
        )

        # Cambiar x^1 por x
        polinomio_str = polinomio_str.replace("x^1", "x")

        # Evaluar el polinomio en x_eval
        f_x_eval = sum(coef * (x_eval ** i) for i, coef in enumerate(coeficientes))

        # Generar la gráfica
        imagen_path = generar_grafica(x, y, coeficientes)

        # Convertir resultados a HTML (con 4 decimales)
        resultado_html = convertir_resultado_a_html(polinomio_str, x_eval, f_x_eval, imagen_path)
        return {'resultado': resultado_html}, None

    except Exception as e:
        return {'error': f'Error en la interpolación: {str(e)}'}, 500

def generar_grafica(x, y, coeficientes):
    """Genera la gráfica de la interpolación y la guarda como imagen."""
    # Crear un rango de valores X para la gráfica
    x_range = np.linspace(min(x) - 1, max(x) + 1, 1000)
    
    # Evaluar el polinomio en estos puntos
    y_range = sum(coef * (x_range ** i) for i, coef in enumerate(coeficientes))
    
    # Crear la gráfica
    plt.figure(figsize=(8, 6))
    plt.plot(x_range, y_range, label="Polinomio Interpolador", color='blue')
    plt.scatter(x, y, color='red', zorder=5, label="Puntos dados")
    plt.title('Interpolación por Sistemas Matriciales')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    # Guardar la imagen en el servidor
    image_path = 'static/grafica_interpolacion.png'
    plt.savefig(image_path)
    plt.close()

    return image_path

def convertir_resultado_a_html(polinomio, x_eval, resultado, imagen_path):
    """Convierte el polinomio, la evaluación y la imagen de la gráfica en HTML."""
    html = f"""
    <h2>Polinomio Interpolador:</h2>
    <p>{polinomio.replace("+ -", "- ")}</p>
    <h2>Evaluación en x = {x_eval}:</h2>
    <p>f({x_eval}) = {resultado:.4f}</p>
    <h2>Gráfica:</h2>
    <img src="{imagen_path}" alt="Gráfica de la Interpolación">
    """
    return html
