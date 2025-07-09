console.log("perfil.js")
// Django's Recommended getCookie Function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let timeout1 = null;
let timeout2 = null;

function inputListener(timeout, elementStatus, path) {
    return function() {
        clearTimeout(timeout);

        const input = this;
        const value = input.value;
        const displayStatus = document.getElementById(elementStatus)
        //console.log("listener "+path)

        timeout = setTimeout(() => {
            fetch(window.location.pathname + path, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    value: value
                })
            })
            .then(response => response.json())
            .then(data => {
                //console.log('Saved:', data);
                displayStatus.textContent = "✔ Guardado";
                setTimeout(() => {
                    displayStatus.textContent = "";
                }, 1000);
            })
            .catch(error => {
                console.error('Error:', error);
                displayStatus.textContent = "⚠ Error";
            });
        }, 1000); // 500 ms debounce, frecuencia de guardado
    };
}

document.getElementById('comentarios').addEventListener("input", inputListener(timeout1, 'status', '/comentarios'));
document.getElementById('entradaHoy').addEventListener("input", inputListener(timeout2, 'statusEntrada', '/entrada'));


cargaDatos = document.getElementById('cargaDatos')
displayDatos = document.getElementById('displayDatos')

function toggle() {
    if(cargaDatos.style.visibility == 'hidden'){
        cargaDatos.style = 'visibility: visible; position: initial'
        displayDatos.style = 'visibility: hidden; position: absolute'
    }
    else{
        cargaDatos.style = 'visibility: hidden; position: absolute'
        displayDatos.style = 'visibility: visible; position: initial'
    }
        
}

document.getElementById("cambiar").addEventListener("click", toggle);


