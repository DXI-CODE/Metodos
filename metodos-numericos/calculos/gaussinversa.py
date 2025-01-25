
def convertir_matriz_a_html(matriz):
    """Convierte una matriz NumPy en una tabla HTML."""
    filas = ""
    for fila in matriz:
        filas += "<tr>" + "".join(f"<td>{round(valor, 4)}</td>" for valor in fila) + "</tr>"
    return f"<table border='1' style='border-collapse: collapse;'>{filas}</table>"