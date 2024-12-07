// Abrir modal de agregar sensor
function openAgregarSensor() {
    document.getElementById('agregarSensorModal').style.display = 'flex';
}

// Abrir modal de edición y cargar datos del sensor
function openEditarSensor(id_sensor) {
    fetch(`/sensores/${id_sensor}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            document.getElementById('edit_id_sensor').value = data.id_sensor;
            document.getElementById('edit_nombre').value = data.nombre;
            document.getElementById('edit_id_institucion').value = data.id_institucion;
            document.getElementById('edit_tipo_sensor').value = data.tipo_sensor;

            filtrarPisosPorInstitucion('edit_');

            setTimeout(() => {
                document.getElementById('edit_id_piso').value = data.id_piso;
                filtrarUbicacionesPorPiso(data.id_piso, 'edit_');
            }, 500);

            document.getElementById('editarSensorModal').style.display = 'flex';
        })
        .catch(error => console.error('Error al obtener los datos del sensor:', error));
}

// Abrir modal de eliminación de sensor
function openEliminarSensor(id_sensor) {
    document.getElementById('delete_id_sensor').value = id_sensor;
    document.getElementById('eliminarSensorModal').style.display = 'flex';
}

// Cerrar modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Filtrar pisos por institución
function filtrarPisosPorInstitucion(tipo = '') {
    const institucionSelect = document.getElementById(`${tipo}id_institucion`);
    const pisoSelect = document.getElementById(`${tipo}id_piso`);

    if (!institucionSelect) {
        console.error(`No se encontró el select con id="${tipo}id_institucion"`);
        return;
    }

    const idInstitucion = institucionSelect.value;

    if (!idInstitucion) {
        console.error('Debe seleccionar una institución.');
        return;
    }

    fetch(`/obtener_pisos/${idInstitucion}`)
        .then(response => response.json())
        .then(data => {
            if (data.pisos) {
                pisoSelect.innerHTML = '<option value="">Seleccione un piso</option>';
                data.pisos.forEach(piso => {
                    const option = document.createElement('option');
                    option.value = piso.id_piso;
                    option.textContent = piso.nombre;
                    pisoSelect.appendChild(option);
                });
            } else {
                console.warn('No se encontraron pisos para esta institución.');
            }
        })
        .catch(error => console.error('Error al cargar los pisos:', error));
}

// Filtrar ubicaciones por piso
function filtrarUbicacionesPorPiso(idPiso = '', tipo = '') {
    if (!idPiso) {
        console.error('Debe seleccionar un piso');
        return;
    }

    fetch(`/obtener_ubicaciones/${idPiso}`)
        .then(response => response.json())
        .then(data => {
            const ubicacionSelect = document.getElementById(`${tipo}id_ubicacion`);
            ubicacionSelect.innerHTML = '<option value="">Seleccione una ubicación</option>';

            if (data.length > 0) {
                data.forEach(ubicacion => {
                    const option = document.createElement('option');
                    option.value = ubicacion.id_ubicacion;
                    option.textContent = ubicacion.nombre;
                    ubicacionSelect.appendChild(option);
                });
            } else {
                console.warn('No se encontraron ubicaciones para este piso.');
            }
        })
        .catch(error => console.error('Error al cargar las ubicaciones:', error));
}

function cambiarEstadoSensor(id_sensor, nuevoEstado) {
    console.log(`Cambiando estado del sensor ${id_sensor} a ${nuevoEstado}`); // Depuración

    fetch(`/cambiar_estado_sensor/${id_sensor}`, {
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
            alert(`El sensor ha sido ${nuevoEstado}`);
            location.reload();  // Recargar la página para reflejar el cambio
        } else {
            console.error('Error en el cambio de estado:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

