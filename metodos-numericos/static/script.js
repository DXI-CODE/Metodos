document.getElementById('formulario').addEventListener('submit', function (e) {
    e.preventDefault();

    const puntosTexto = document.getElementById('puntos').value.trim();
    const puntos = puntosTexto
        .split('\n') // Dividir el contenido en líneas
        .map(linea => linea.split(',').map(Number)) // Dividir cada línea en x, y
        .filter(par => par.length === 2 && !isNaN(par[0]) && !isNaN(par[1])); // Filtrar pares válidos

    if (puntos.length < 2) {
        document.getElementById('resultado').innerText = "Por favor ingresa al menos dos puntos válidos.";
        return;
    }

    fetch('/calcular', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ puntos }), // Enviar los puntos al back-end
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                document.getElementById('resultado').innerText = `Error: ${data.error}`;
            } else {
                document.getElementById('resultado').innerText = `Función Interpolada: ${data.funcion}`;
            }
        })
        .catch((error) => console.error('Error:', error));
});
