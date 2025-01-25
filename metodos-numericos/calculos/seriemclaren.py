import sympy as sp

def calcular_serie_mclaren(funcion_str, expansion, numero_n):
    """
    Calcula la serie de McLaren de una función dada.

    Args:
    - funcion_str (str): La función como cadena, por ejemplo, 'sin(x)'
    - expansion (float): El valor alrededor del cual expandir (a)
    - numero_n (int): Número de términos en la expansión (n)

    Returns:
    - str: Expansión en serie de McLaren en formato LaTeX
    """

    # Crear la variable simbólica x
    x = sp.symbols('x')

    # Convertir la función de cadena a una función simbólica
    try:
        funcion = sp.sympify(funcion_str)
    except sp.SympifyError:
        raise ValueError("La función proporcionada no es válida.")

    # Calcular la serie de McLaren (expansión alrededor de 'expansion')
    serie_mclaren = sp.series(funcion, x, expansion, numero_n).removeO()

    # Convertir la serie a formato LaTeX para MathJax
    return sp.latex(serie_mclaren)
