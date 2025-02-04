import sympy as sp

def calcular_serie_mclaurin(funcion_str, numero_n):
    expansion = 0.0
    x = sp.symbols('x')
    funcion = sp.sympify(funcion_str)
    serie_maclaurin = sp.series(funcion, x, expansion, numero_n)
    
    serie_latex = sp.latex(serie_maclaurin)
    serie_latex = serie_latex.replace('**', '^').replace('O(', 'O(')
    return serie_latex
    #return str(serie_latex).replace('**', '^').replace('O(', 'O(')
