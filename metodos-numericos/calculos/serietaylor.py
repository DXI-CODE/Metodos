import sympy as sp

def calcular_serie_taylor(funcion_str, expansion, numero_n):
    x = sp.symbols('x')
    funcion = sp.sympify(funcion_str)
    serie_taylor = sp.series(funcion, x, expansion, numero_n)
    
    serie_latex = sp.latex(serie_taylor)
    serie_latex = serie_latex.replace('**', '^').replace('O(', 'O(')
    return serie_latex
    #return str(serie_latex).replace('**', '^').replace('O(', 'O(')
