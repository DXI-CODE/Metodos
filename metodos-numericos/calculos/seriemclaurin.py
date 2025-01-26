from sympy import symbols, sympify, diff, factorial, latex

def calcular_serie_mclaurin(function_str, numero_n):
    """
    Calcula la serie de Maclaurin (una expansión en serie de Taylor en a=0) de una función dada.

    Args:
        function_str (str): La función a expandir, expresada como una cadena de texto.
        numero_n (int): El número de términos a calcular en la serie de Maclaurin.

    Returns:
        str: La expansión de la serie de Maclaurin en formato LaTeX.
    """
    # Variables simbólicas
    x = symbols('x')
    
    # Convierte el string de la función a una expresión simbólica
    function = sympify(function_str)

    # Calcula la serie de Maclaurin (a = 0)
    maclaurin_expansion = 0
    for i in range(numero_n):
        # Derivada de orden i
        derivative = diff(function, x, i)
        
        # Termino i-ésimo de la serie de Maclaurin
        term = (derivative.subs(x, 0) / factorial(i)) * (x)**i
        maclaurin_expansion += term

    print(maclaurin_expansion)
    print(latex(maclaurin_expansion))
    # Devuelve el resultado como un string LaTeX
    return latex(maclaurin_expansion)
