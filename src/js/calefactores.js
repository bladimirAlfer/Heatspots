// Abrir modal de agregar sensor
function openAgregarCalefactor() {
    document.getElementById('agregarCalefactorModal').style.display = 'flex';
}

// Función para abrir el modal de edición y cargar los datos del calefactor
function openEditarCalefactor(id_calefactor) {
    fetch(`/calefactores/${id_calefactor}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            document.getElementById('edit_nombre').value = data.nombre;
            document.getElementById('editar_id_institucion').value = data.id_institucion;
            document.getElementById('edit_id').value = data.id_calefactor;

            // Llenar el select de pisos según la institución seleccionada
            filtrarPisosPorInstitucion('editar');

            // Espera un tiempo para que se carguen los pisos antes de seleccionar el piso actual
            setTimeout(() => {
                document.getElementById('editar_id_piso').value = data.id_piso;
                filtrarUbicacionesPorPiso(data.id_piso, 'editar');
            }, 500);

            document.getElementById('editar_id_ubicacion').value = data.id_ubicacion;

            document.getElementById('editarCalefactorModal').style.display = 'flex';
        })
        .catch(error => console.error('Error al obtener los datos del calefactor:', error));
}




function openEliminarCalefactor(id_calefactor) {
    document.getElementById('delete_id_calefactor').value = id_calefactor;
    document.getElementById('eliminarCalefactorModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Función para filtrar pisos por institución
function filtrarPisosPorInstitucion(tipo) {
    const institucionSelect = document.getElementById(`${tipo}_id_institucion`);
    const idInstitucion = institucionSelect.value;
    const pisoSelect = document.getElementById(`${tipo}_id_piso`);
    const ubicacionSelect = document.getElementById(`${tipo}_id_ubicacion`);

    // Limpiar los selects anteriores
    pisoSelect.innerHTML = '<option value="">Selecciona un piso</option>';
    ubicacionSelect.innerHTML = '<option value="">Selecciona una ubicación</option>';

    if (!idInstitucion) {
        console.error('Debe seleccionar una institución.');
        return;
    }

    // Obtener los pisos filtrados por la institución
    fetch(`/obtener_pisos/${idInstitucion}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.pisos) {
                data.pisos.forEach(piso => {
                    const option = document.createElement('option');
                    option.value = piso.id_piso;
                    option.textContent = piso.nombre;
                    pisoSelect.appendChild(option);
                });
            } else {
                console.error('No se encontraron pisos para esta institución.');
            }
        })
        .catch(error => console.error('Error al cargar los pisos:', error));

    // Asociar el evento change para cargar las ubicaciones cuando se selecciona un piso
    pisoSelect.addEventListener('change', () => {
        const idPiso = pisoSelect.value;
        ubicacionSelect.innerHTML = '<option value="">Selecciona una ubicación</option>';

        if (!idPiso) {
            console.error('Debe seleccionar un piso.');
            return;
        }

        fetch(`/obtener_ubicaciones/${idPiso}`)
            .then(response => response.json())
            .then(data => {
                if (data && Array.isArray(data)) {
                    data.forEach(ubicacion => {
                        const option = document.createElement('option');
                        option.value = ubicacion.id_ubicacion;
                        option.textContent = ubicacion.nombre;
                        ubicacionSelect.appendChild(option);
                    });
                } else {
                    console.error('No se encontraron ubicaciones para este piso.');
                }
            })
            .catch(error => console.error('Error al cargar las ubicaciones:', error));
    });
}


function filtrarUbicacionesPorPiso(idPiso, tipo) {
    // Asegúrate de que el ID de piso es válido
    if (!idPiso) {
        console.error('Debe seleccionar un piso');
        return;
    }

    fetch(`/obtener_ubicaciones/${idPiso}`)
        .then(response => response.json())
        .then(data => {
            const ubicacionSelect = document.getElementById(`${tipo}_id_ubicacion`);
            
            // Vaciar las ubicaciones anteriores
            ubicacionSelect.innerHTML = '<option value="">Selecciona una ubicación</option>';

            if (data && Array.isArray(data)) {
                // Usar forEach solo si es un arreglo válido
                data.forEach(ubicacion => {
                    const option = document.createElement('option');
                    option.value = ubicacion.id_ubicacion;
                    option.textContent = ubicacion.nombre;
                    ubicacionSelect.appendChild(option);
                });
            } else {
                console.error('No se encontraron ubicaciones para este piso.');
            }
        })
        .catch(error => console.error('Error al cargar las ubicaciones:', error));
}

function cambiarEstadoCalefactor(id_calefactor, nuevoEstado) {
    console.log(`Cambiando estado del calefactor ${id_calefactor} a ${nuevoEstado}`); // Depuración

    fetch(`/cambiar_estado_calefactor/${id_calefactor}`, {
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
            alert(`El calefactor ha sido ${nuevoEstado}`);
            location.reload();  // Recargar la página para reflejar el cambio
        } else {
            console.error('Error en el cambio de calefactor:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}
