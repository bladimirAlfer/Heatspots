function cambiarEstadoReporte(id_reporte, nuevoEstado) {
    console.log(`Cambiando estado del reporte ${id_reporte} a ${nuevoEstado}`); // Depuración

    fetch(`/cambiar_estado_reporte/${id_reporte}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ estado: nuevoEstado })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(`El reporte ha sido marcado como ${nuevoEstado}`);
                location.reload(); // Recargar la página para reflejar el cambio
            } else {
                console.error('Error en el cambio de estado del reporte:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

function openEliminarModal(idReporte) {
    document.getElementById('delete_id_reporte').value = idReporte;
    document.getElementById('eliminarReporteModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}
