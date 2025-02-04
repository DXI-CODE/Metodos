import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sympy import symbols, sympify, SympifyError


def runge_kutta_4(ecuaciones, variables, x0, valores_iniciales, h, n):
    """
    Método de Runge-Kutta de orden 4 para sistemas de ecuaciones diferenciales.

    Args:
        ecuaciones (list[str]): Lista de ecuaciones diferenciales en formato str.
        variables (list[str]): Lista de variables dependientes (por ejemplo, ['y', 'z', 'm']).
        x0 (float): Valor inicial de x.
        valores_iniciales (list[float]): Valores iniciales de las variables dependientes.
        h (float): Tamaño del paso.
        n (int): Número de pasos.

    Returns:
        dict: Contiene los últimos valores de las variables y la gráfica (base64).
    """

    if len(ecuaciones) != len(variables):
        raise ValueError("El número de ecuaciones debe coincidir con el número de variables.")

    x = sp.Symbol('x')
    variables_syms = [sp.Symbol(var) for var in variables]
    ecuaciones_syms = [sp.sympify(ec) for ec in ecuaciones]

    # Convertir las ecuaciones en funciones de Python
    funciones = [sp.lambdify([x, *variables_syms], ec) for ec in ecuaciones_syms]

    # Valores iniciales
    resultados = [[x0] + valores_iniciales]

    for _ in range(n):
        x_actual = resultados[-1][0]
        y_actual = np.array(resultados[-1][1:])

        # Calcular k1, k2, k3, k4 para cada ecuación
        k1 = np.array([h * f(x_actual, *y_actual) for f in funciones])
        k2 = np.array([h * f(x_actual + h / 2, *(y_actual + k1 / 2)) for f in funciones])
        k3 = np.array([h * f(x_actual + h / 2, *(y_actual + k2 / 2)) for f in funciones])
        k4 = np.array([h * f(x_actual + h, *(y_actual + k3)) for f in funciones])

        # Actualizar las variables dependientes
        y_siguiente = y_actual + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x_siguiente = x_actual + h

        # Agregar el nuevo punto a los resultados
        resultados.append([x_siguiente, *y_siguiente])

    # Tomar los últimos valores de las evaluaciones
    print("Tomando los últimos valores de las evaluaciones...")
    ultimos_valores = []
    for i in range(len(variables)):
        valor = resultados[-1][i + 1]
        if isinstance(valor, sp.Basic):
            try:
                # Evaluamos completamente la expresión simbólica
                valor = valor.evalf()
                print(f"Valor evaluado (tipo sympy.Basic): {valor}")
            except Exception as e:
                print(f"Error al evaluar el valor de la variable {variables[i]}: {e}")
                valor = float(valor)  # Forzar la conversión
        else:
            print(f"Valor directo (tipo no SymPy): {valor}")
        
        try:
            # Intentamos convertir a float
            valor_float = round(float(valor), 4)
            ultimos_valores.append(valor_float)
            print(f"Valor de {variables[i]} (convertido a float): {valor_float}")
        except Exception as e:
            print(f"Error al convertir el valor de {variables[i]} a float: {e}")

    print(f"Últimos valores: {ultimos_valores}")




    # Generar la gráfica
    print("Generando la gráfica...")
    try:
        fig, ax = plt.subplots()
        for i, var in enumerate(variables):
            print(f"Graficando {var}(x)...")
            ax.plot([fila[0] for fila in resultados],
                    [fila[i + 1] for fila in resultados],
                    label=f'{var}(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('Valores')
        ax.legend()
        ax.set_title('Método de Runge-Kutta de Orden 4')

        # Convertir gráfica a base64
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        grafico_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close(fig)

        print("Gráfica generada correctamente.")
    except Exception as e:
        print(f"Error al generar la gráfica: {e}")
        grafico_base64 = None

    return {'ultimos_valores': ultimos_valores, 'grafico_base64': grafico_base64}



def validar_ecuaciones(ecuaciones, variables):
    """
    Valida y convierte las ecuaciones ingresadas a expresiones SymPy.

    Args:
        ecuaciones (list): Lista de ecuaciones ingresadas como cadenas.
        variables (list): Lista de variables dependientes.

    Returns:
        list: Lista de expresiones SymPy.

    Raises:
        ValueError: Si alguna ecuación es inválida.
    """
    try:
        # Reemplazar "^" con "**" para asegurar la sintaxis correcta
        ecuaciones = [eq.replace("^", "**") for eq in ecuaciones]

        # Crear símbolos para x y las variables dependientes
        simbolos = symbols("x " + " ".join(variables))

        # Asegurarse de que 'e' se defina correctamente como la constante de Euler
        locals_dict = {str(s): s for s in simbolos}
        locals_dict['e'] = sp.E  # Definir 'e' como la constante de Euler

        # Validar ecuaciones, usando el diccionario local que incluye 'e'
        ecuaciones_sympy = [sympify(eq, locals=locals_dict) for eq in ecuaciones]
        return ecuaciones_sympy
    except Exception as e:
        raise ValueError(f"Error en la validación de la ecuación: {str(e)}")

