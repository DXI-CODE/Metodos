document.getElementById('formulario').addEventListener('submit', function(e) {
    e.preventDefault();

    // Obtener los valores de los inputs
    const funcion = document.getElementById('funcion').value;
    const expansion = parseFloat(document.getElementById('expansion').value);
    const numero_n = parseInt(document.getElementById('numero_n').value);

    // Verificar que todos los campos sean correctos
    if (isNaN(expansion) || isNaN(numero_n) || numero_n <= 0) {
        document.getElementById('ResultadoSerieTaylor').innerHTML = "Por favor, ingrese valores válidos para el punto de expansión y el número de términos.";
        return;
    }

    // Crear el objeto de datos que se enviará al servidor
    const datos = {
        funcion: funcion,
        expansion: expansion,
        numero_n: numero_n
    };

    // Enviar los datos al servidor utilizando fetch
    fetch('/calcular_taylor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.funcion_taylor) {
            document.getElementById('ResultadoSerieTaylor').innerHTML = `Serie de Taylor: ${data.funcion_taylor}`;
        } else if (data.error) {
            document.getElementById('ResultadoSerieTaylor').innerHTML = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        document.getElementById('ResultadoSerieTaylor').innerHTML = `Error: ${error.message}`;
    });
});
