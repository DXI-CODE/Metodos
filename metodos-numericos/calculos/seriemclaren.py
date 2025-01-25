from sympy import symbols, sympify, diff, factorial

def calcular_serie_mclaren(function_str, numero_n):
    # Variables simbólicas
    x = symbols('x')
    function = sympify(function_str)  # Convierte el string en una expresión simbólica
    print(function)

    # Calcula la serie de Maclaurin (a = 0)
    a = 0
    maclaurin_expansion = 0
    for i in range(numero_n):
        derivative = diff(function, x, i)  # Derivada de orden i
        term = (derivative.subs(x, a) / factorial(i)) * (x - a)**i
        maclaurin_expansion += term
    print(maclaurin_expansion)

    # Devuelve el resultado como string en formato legible
    return str(maclaurin_expansion).replace('**', '^')
