function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ocultarInmueble(inmuebleId) {
    if (confirm('¿Estás seguro de que quieres ocultar este inmueble?')) {
        fetch(`/ocultar_inmueble/${inmuebleId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error al ocultar el inmueble.');
            }
        });
    }
}


function mostrarInmueble(inmuebleId) {
    if (confirm('¿Estás seguro de que quieres mostrar este inmueble?')) {
        fetch(`/mostrar_inmueble/${inmuebleId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error al mostrar el inmueble.');
            }
        });
    }
}

function eliminarInmueble(inmuebleId) {
    if (confirm('¿Estás seguro de que quieres eliminar este inmueble?')) {
        fetch(`/eliminar_inmueble/${inmuebleId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error al eliminar el inmueble.');
            }
        });
    }
}


function aceptarSolicitud(solicitudId) {
    if (confirm('¿Estás seguro de que quieres aceptar esta solicitud?')) {
        fetch(`/aceptar_solicitud/${solicitudId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('Solicitud aceptada');
                location.reload();
            } else {
                alert('Error al aceptar la solicitud.');
            }
        });
    }
}

function rechazarSolicitud(solicitudId) {
    if (confirm('¿Estás seguro de que quieres rechazar esta solicitud?')) {
        fetch(`/rechazar_solicitud/${solicitudId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('Solicitud rechazada');
                location.reload();
            } else {
                alert('Error al rechazar la solicitud.');
            }
        });
    }
}

