import numpy as np
from sklearn.linear_model import LinearRegression

def calcular_regresion(X, y):
    try:
        X = np.array(X)
        y = np.array(y)

        modelo = LinearRegression()
        modelo.fit(X, y)

        coeficientes = modelo.coef_.tolist()
        intercepto = modelo.intercept_

        ecuacion = "y = "
        for i, coef in enumerate(coeficientes):
            if coef >= 0 and i > 0:
                ecuacion += f" + {coef:.4f} \\cdot x_{{{i+1}}}"
            elif coef < 0:
                ecuacion += f" - {abs(coef):.4f} \\cdot x_{{{i+1}}}"
            else:
                ecuacion += f"{coef:.4f} \\cdot x_{{{i+1}}}"

        ecuacion += f" + {intercepto:.4f}"

        return {
            "coeficientes": coeficientes,
            "intercepto": intercepto,
            "ecuacion_latex": ecuacion  
        }
    except Exception as e:
        return {"error": str(e)}
