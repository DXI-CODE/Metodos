import sympy as sp
import math

def simpson1_3(funcion, x0, xn, numero_n):
    if(xn <= x0):
        raise ValueError('El límite superior debe ser mayor al límite inferior')
    
    if(numero_n <= 0):
        raise ValueError('El número de términos debe ser mayor a 0')
    
    if(numero_n % 2 == 1):
        raise ValueError('El número de términos debe ser un número par')
    
    context = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'sqrt': math.sqrt,
        'pi': math.pi
    }

    def g(x):
        return eval(funcion, {"x": x}, context)
    
    x = sp.symbols('x')
    ##function = sp.lambdify(x, funcion, 'numpy')  # Convierte el string en una expresión simbólica

    h = (xn - x0) / numero_n

    sum = 0
    for i in range(0,(numero_n-2),2):
        xi = x0 + i*h
        xi2 = x0 + (i+1)*h
        sum += 4*g(xi) + 2*g(xi2)
    xh = xn - h
    sum += 4*g(xh) + g(xn)

    return (h*sum)/3