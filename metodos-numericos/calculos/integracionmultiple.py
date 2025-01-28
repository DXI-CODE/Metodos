import numpy as np
import sympy as sp
import re

def simpson1_3(funcion, x0, xn, numero_n, simbolo):
    # Check if the limits and number of terms are valid
    if xn <= x0:
        print(x0)
        print(xn)
        raise ValueError('El límite superior debe ser mayor al límite inferior')
    
    if numero_n <= 0:
        raise ValueError('El número de términos debe ser mayor a 0')
    
    if numero_n % 2 == 1:
        raise ValueError('El número de términos debe ser un número par')
    
    # Define symbolic variable
    x = sp.symbols(simbolo)
    
    # Ensure the function is a symbolic expression
    funcion = sp.sympify(funcion)
    
    # Step size (h)
    h = (xn - x0) / numero_n
    
    # Initialize sum
    total_sum = 0
    
    # Simpson's 1/3 rule loop
    for i in range(0, numero_n - 1, 2):  # Step by 2 for Simpson's rule
        xi = x0 + i * h
        xi2 = x0 + (i + 1) * h
        total_sum += 4 * funcion.subs(x, xi) + 2 * funcion.subs(x, xi2)
    
    # Add the last terms (evaluating at xn and using the last step)
    xh = x0 + (numero_n - 1) * h
    total_sum += 4 * funcion.subs(x, xh) + funcion.subs(x, xn)
    
    # Final symbolic result
    result = (h * total_sum) / 3
    return result

def preprocess_expression(func_str):
    # Ensure multiplication is explicit in expressions like 'yz' or '3y'
    # Match cases like '3y' or 'yz' and insert the multiplication operator
    func_str = re.sub(r'([a-zA-Z])([0-9])', r'\1*\2', func_str)  # Handles cases like '3y' -> '3*y'
    func_str = re.sub(r'([0-9])([a-zA-Z])', r'\1*\2', func_str)  # Handles cases like '3x' -> '3*x'
    func_str = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', func_str)  # Handles cases like 'yz' -> 'y*z'
    return func_str

def integracionmultiple(funcion, x0, xn, variables, numero_n, cantidad_integraciones):
    if cantidad_integraciones <= 0 and cantidad_integraciones > 4:
        raise ValueError('El número de integraciones debe estar entre 2 y 4')

    if len(variables) != (len(x0)-1) and len(variables) != (len(xn)-1):
        raise ValueError('El número de variables no corresponde al número de límites')
    
    if cantidad_integraciones != len(x0) and cantidad_integraciones != len(xn):
        raise ValueError('El número de integraciones debe ser igual al número de límites tanto superiores como inferiores')

    func = preprocess_expression(funcion)
    variables.insert(0,'x')
    
    for i in range(len(variables)):
        func = simpson1_3(func, x0[i], xn[i], numero_n, variables[i])
        print(str(func))


    return func.evalf()
