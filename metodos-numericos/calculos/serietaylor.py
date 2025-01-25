import sympy as sp

def calcular_serie_taylor(funcion_str, expansion, numero_n):
    x = sp.symbols('x')
    funcion = sp.sympify(funcion_str)
    serie_taylor = sp.series(funcion, x, expansion, numero_n)
    return str(serie_taylor).replace('**', '^').replace('O(', 'O(')
