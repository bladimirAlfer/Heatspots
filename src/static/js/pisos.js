// Función para abrir el modal de agregar un piso
function openAgregarPiso() {
    document.getElementById('agregarPisoModal').style.display = 'flex';
}

// Función para abrir el modal de editar piso
function openEditarPiso(id_piso) {
    // Realizar una petición para obtener los datos del piso
    fetch(`/piso/${id_piso}`)
        .then(response => response.json())
        .then(data => {
            // Rellenar el formulario de edición con los datos obtenidos
            document.getElementById('edit_id_piso').value = data.id_piso;
            document.getElementById('edit_nombre').value = data.nombre;
            document.getElementById('edit_id_institucion').value = data.id_institucion;
            // Opcional: manejar vista previa de imagen existente
            document.getElementById('editarPisoModal').style.display = 'flex';
        })
        .catch(error => console.error('Error al obtener los datos del piso:', error));
}

// Función para abrir el modal de eliminar un piso
function openEliminarPiso(id_piso) {
    document.getElementById('delete_id_piso').value = id_piso;
    document.getElementById('eliminarPisoModal').style.display = 'flex';
}


// Función para cerrar cualquier modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}
