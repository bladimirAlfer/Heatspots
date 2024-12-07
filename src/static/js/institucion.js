function openAgregarInstitucion() {
    document.getElementById('agregarInstitucionModal').style.display = 'block';
}

function openEditarInstitucion(id_institucion) {
    // Realizar una petición para obtener los datos de la institución
    fetch(`/institucion/${id_institucion}`)
        .then(response => response.json())
        .then(data => {
            // Rellenar el formulario de edición con los datos obtenidos
            document.getElementById('edit_nombre').value = data.nombre;
            document.getElementById('edit_descripcion').value = data.descripcion;
            // Manejo del logo omitido para simplificación
            document.getElementById('edit_id').value = data.id_institucion; // Usamos el ID para el formulario
            document.getElementById('editarInstitucionModal').style.display = 'block';
        })
        .catch(error => console.error('Error al obtener los datos de la institución:', error));
}


function openEliminarInstitucion(id_institucion) {
    document.getElementById('eliminarInstitucionModal').style.display = 'block';
    document.getElementById('delete_id').value = id_institucion;
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

