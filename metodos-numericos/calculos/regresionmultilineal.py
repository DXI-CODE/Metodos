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

        return {
            "coeficientes": coeficientes,
            "intercepto": intercepto
        }
    except Exception as e:
        return {"error": str(e)}
