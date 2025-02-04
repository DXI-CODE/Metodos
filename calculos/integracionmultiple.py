import sympy as sp


def simpson1_3(funcion, x0, xn, numero_n, simbolo):
    if xn <= x0:
        print(x0)
        print(xn)
        raise ValueError('El límite superior debe ser mayor al límite inferior')
    
    if numero_n <= 0:
        raise ValueError('El número de términos debe ser mayor a 0')
    
    if numero_n % 2 == 1:
        raise ValueError('El número de términos debe ser un número par')
    
    x = sp.symbols(simbolo)

    funcion = sp.sympify(funcion)
    
    h = (xn - x0) / numero_n
    
    total_sum = 0
    
    for i in range(0, numero_n - 1, 2):  
        xi = x0 + i * h
        xi2 = x0 + (i + 1) * h
        total_sum += 4 * funcion.subs(x, xi) + 2 * funcion.subs(x, xi2)
    
    xh = x0 + (numero_n - 1) * h
    total_sum += 4 * funcion.subs(x, xh) + funcion.subs(x, xn)
    
    result = (h * total_sum) / 3
    return result

def integracionmultiple(func, x0, xn, variables, numero_n, cantidad_integraciones):
    if cantidad_integraciones <= 0 and cantidad_integraciones > 4:
        raise ValueError('El número de integraciones debe estar entre 2 y 4')

    if len(variables) != (len(x0)-1) and len(variables) != (len(xn)-1):
        raise ValueError('El número de variables no corresponde al número de límites')
    
    if cantidad_integraciones != len(x0) and cantidad_integraciones != len(xn):
        raise ValueError('El número de integraciones debe ser igual al número de límites tanto superiores como inferiores')

    variables.insert(0,'x')
    
    for i in range(len(variables)):
        func = simpson1_3(func, x0[i], xn[i], numero_n, variables[i])
        print(str(func))


    return func.evalf(4)
