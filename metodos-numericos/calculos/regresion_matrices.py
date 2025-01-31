import numpy as np
import matplotlib.pyplot as plt
import base64
import io

def regresion_por_matrices(tipo, x, y):
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x2 = np.sum(x**2)
    sum_x3 = np.sum(x**3)
    sum_x4 = np.sum(x**4)
    sum_xy = np.sum(x * y)
    sum_x2y = np.sum(x**2 * y)
    
    # Manejo de regresión lineal, cuadrática y cúbica
    try:
        if tipo == 'lineal':
            A = np.array([[n, sum_x], [sum_x, sum_x2]])
            C = np.array([sum_y, sum_xy])
        elif tipo == 'cuadratica':
            A = np.array([[n, sum_x, sum_x2], [sum_x, sum_x2, sum_x3], [sum_x2, sum_x3, sum_x4]])
            C = np.array([sum_y, sum_xy, sum_x2y])
        elif tipo == 'cubica':
            A = np.array([[n, sum_x, sum_x2, sum_x3], [sum_x, sum_x2, sum_x3, sum_x4], 
                          [sum_x2, sum_x3, sum_x4, np.sum(x**5)], [sum_x3, sum_x4, np.sum(x**5), np.sum(x**6)]])
            C = np.array([sum_y, sum_xy, sum_x2y, np.sum(x**3 * y)])
        else:
            raise ValueError('Tipo de regresión no reconocido.')

        # Intentar resolver el sistema de ecuaciones
        a = np.linalg.solve(A, C)

        # Cálculo de valores ajustados
        y_cal = np.polyval(np.flip(a), x)
        
        # Errores
        st = np.sum((y - np.mean(y))**2)
        sr = np.sum((y - y_cal)**2)
        r2 = (st - sr) / st

        # Crear tabla HTML
        tabla_html = """
        <table border="1">
            <tr>
                <th>x</th><th>y</th><th>x²</th><th>xy</th><th>ŷ</th><th>St</th><th>Sr</th>
            </tr>
        """
        
        for i in range(n):
            st_i = (y[i] - np.mean(y))**2
            sr_i = (y[i] - y_cal[i])**2
            tabla_html += f"""
            <tr>
                <td>{x[i]:.4f}</td><td>{y[i]:.4f}</td><td>{x[i]**2:.4f}</td>
                <td>{x[i] * y[i]:.4f}</td><td>{y_cal[i]:.4f}</td>
                <td>{st_i:.4f}</td><td>{sr_i:.4f}</td>
            </tr>
            """
        
        tabla_html += f"""
            <tr>
                <td><b>Σ</b></td><td>{sum_y:.4f}</td><td>{sum_x2:.4f}</td>
                <td>{sum_xy:.4f}</td><td>-</td><td>{st:.4f}</td><td>{sr:.4f}</td>
            </tr>
        </table>
        <p>a0 = {a[0]:.4f}</p>
        <p>a1 = {a[1]:.4f}</p>
        <p>a2 = {a[2]:.4f}</p>
        <p>a3 = {a[3]:.4f}</p>
        <p>St = {st:.4f}</p>
        <p>Sr = {sr:.4f}</p>
        <p>r² = {r2:.4f}</p>
        """

        # Generar gráfico
        plt.figure(figsize=(6, 4))
        plt.scatter(x, y, color='blue', label='Datos originales')

        # Ajustar el formato según la regresión seleccionada
        if tipo == 'lineal':
            plt.plot(x, y_cal, color='red', linestyle='-', label=f'Regresión: y = {a[0]:.4f} + {a[1]:.4f}x')
        elif tipo == 'cuadratica':
            plt.plot(x, y_cal, color='red', linestyle='-', label=f'Regresión: y = {a[0]:.4f} + {a[1]:.4f}x + {a[2]:.4f}x²')
        elif tipo == 'cubica':
            plt.plot(x, y_cal, color='red', linestyle='-', label=f'Regresión: y = {a[0]:.4f} + {a[1]:.4f}x + {a[2]:.4f}x² + {a[3]:.4f}x³')

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f"Regresión {tipo.capitalize()}")
        plt.legend()
        plt.grid()

        # Guardar imagen en base64 para enviarla al HTML
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        grafico_base64 = base64.b64encode(img.getvalue()).decode()

        return tabla_html, grafico_base64
    
    except np.linalg.LinAlgError as e:
        # Si hay un error en la matriz (por ejemplo, no se puede invertir), lo manejamos aquí.
        return f"Error en la matriz: {str(e)}"
    except ValueError as e:
        return f"Error: {str(e)}"
