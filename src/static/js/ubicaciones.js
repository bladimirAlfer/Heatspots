
    // Función para abrir el modal de agregar ubicación
    function openAgregarUbicacion() {
        document.getElementById('agregarUbicacionModal').style.display = 'flex';
    }

    function openEditarUbicacion(id_ubicacion) {
        fetch(`/ubicaciones/${id_ubicacion}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }
    
                // Rellenamos los campos con los valores obtenidos de la BD
                document.getElementById('edit_id_ubicacion').value = data.id_ubicacion;
                document.getElementById('edit_nombre').value = data.nombre;
                document.getElementById('edit_detalle').value = data.detalle;
                document.getElementById('edit_coordenadas').value = data.coordenadas || '';
    
                // Establece el valor de la institución seleccionada
                document.getElementById('id_institucion').value = data.id_institucion;
    
                // Ahora que el select tiene una institución, podemos filtrar los pisos
                filtrarPisosPorInstitucion('edit');
    
                // No preseleccionamos el piso; el usuario debe seleccionarlo
                document.getElementById('editarUbicacionModal').style.display = 'flex';
            })
            .catch(error => console.error('Error al obtener los datos de la ubicación:', error));
    }
    
    

    // Función para abrir el modal de eliminación
    function openEliminarUbicacion(id_ubicacion) {
        // Asigna el id de la ubicación a eliminar en el formulario de eliminación
        document.getElementById('delete_id_ubicacion').value = id_ubicacion;
        document.getElementById('eliminarUbicacionModal').style.display = 'block';
    }

    function openPlanoModal() {
        const id_piso = document.getElementById('id_piso').value;  // Captura el ID del piso seleccionado
        
        if (!id_piso) {
            console.error('Debe seleccionar un piso primero.');
            return;
        }
    
        // Realiza una solicitud para obtener el plano del piso seleccionado
        fetch(`/get_plano/${id_piso}`)
            .then(response => response.json())
            .then(data => {
                if (data.plano) {
                    // Actualiza la imagen del plano en el modal
                    const plano = document.getElementById('plano');
                    plano.src = `/static/img/uploads/${data.plano}`;
                    document.getElementById('planoModal').style.display = 'block';  // Muestra el modal
                } else {
                    console.error('Error al cargar el plano: Plano no encontrado');
                }
            })
            .catch(error => console.error('Error al cargar el plano:', error));
    }
    

    // Variable para almacenar las coordenadas seleccionadas
    let coordenadasSeleccionadas = '';
    let marcador = null;  // Variable para almacenar el marcador visual

    // Función para agregar el marcador y permitir moverlo
    function agregarMarcador(event) {
        const x = event.offsetX;
        const y = event.offsetY;
        coordenadasSeleccionadas = `${x},${y}`;  // Guardamos las coordenadas

        // Obtener el contenedor del plano
        const planoContainer = document.getElementById('plano-container');

        // Si ya existe un marcador, lo movemos a la nueva ubicación
        if (marcador) {
            marcador.style.top = `${y}px`;
            marcador.style.left = `${x}px`;
        } else {
            // Si no existe, lo creamos
            marcador = document.createElement('div');
            marcador.style.position = 'absolute';
            marcador.style.top = `${y}px`;
            marcador.style.left = `${x}px`;
            marcador.style.width = '10px';
            marcador.style.height = '10px';
            marcador.style.backgroundColor = 'red';
            marcador.style.borderRadius = '50%';
            planoContainer.appendChild(marcador);  // Agregar el marcador al plano
        }
    }

    // Función para guardar las coordenadas en el campo oculto
    function guardarCoordenada() {
        document.getElementById('coordenadas').value = coordenadasSeleccionadas;  // Asignamos la coordenada al input oculto
        console.log('Coordenada guardada:', coordenadasSeleccionadas);
        closeModal('planoModal');
    }

    // Función para abrir el modal del plano y cargar la imagen del plano en el formulario de edición
    function openPlanoModalEdit() {
        const id_piso = document.getElementById('edit_id_piso').value;
    
        if (!id_piso) {
            console.error('Debe seleccionar un piso primero.');
            return;
        }
    
        fetch(`/get_plano/${id_piso}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Verifica lo que está recibiendo el frontend desde el servidor
                if (data.plano) {
                    const plano = document.getElementById('planoEdit');  // Asegúrate de que este es el ID correcto para la imagen del plano en edición
                    plano.src = `/static/img/uploads/${data.plano}`;
                    document.getElementById('planoModalEdit').style.display = 'block';
                } else {
                    console.error('Error al cargar el plano: Plano no encontrado');
                }
            })
            .catch(error => console.error('Error al cargar el plano:', error));
    }
    
    // Variable para almacenar las coordenadas seleccionadas al editar
    let coordenadasSeleccionadasEdit = '';
    let marcadorEdit = null;  // Variable para almacenar el marcador visual al editar

    // Función para agregar el marcador en el modal de edición y permitir moverlo
    function agregarMarcadorEdit(event) {
        const x = event.offsetX;
        const y = event.offsetY;
        coordenadasSeleccionadasEdit = `${x},${y}`;  // Guardamos las coordenadas seleccionadas

        const planoContainerEdit = document.getElementById('plano-container-edit');

        // Si ya existe un marcador, lo movemos a la nueva ubicación
        if (marcadorEdit) {
            marcadorEdit.style.top = `${y}px`;
            marcadorEdit.style.left = `${x}px`;
        } else {
            // Si no existe, lo creamos
            marcadorEdit = document.createElement('div');
            marcadorEdit.style.position = 'absolute';
            marcadorEdit.style.top = `${y}px`;
            marcadorEdit.style.left = `${x}px`;
            marcadorEdit.style.width = '10px';
            marcadorEdit.style.height = '10px';
            marcadorEdit.style.backgroundColor = 'red';
            marcadorEdit.style.borderRadius = '50%';
            planoContainerEdit.appendChild(marcadorEdit);  // Agregar el marcador al plano
        }
    }

    

    function guardarCoordenadaEdit() {
        console.log('Coordenadas editadas guardadas:', coordenadasSeleccionadasEdit);  // Verificar coordenadas
        document.getElementById('edit_coordenadas').value = coordenadasSeleccionadasEdit;  // Asignamos las coordenadas al input oculto
        closeModal('planoModalEdit');
    }
    

    // Función para cerrar cualquier modal
    function closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    function filtrarPisosPorInstitucion(tipo = '') {
        const institucionSelect = document.getElementById(`${tipo ? tipo + '_id_institucion' : 'id_institucion'}`);
        
        if (!institucionSelect) {
            console.error('No se encontró el select de instituciones');
            return;
        }
    
        const idInstitucion = institucionSelect.value;
        
        if (!idInstitucion) {
            console.error('Debe seleccionar una institución primero.');
            return;
        }
    
        fetch(`/obtener_pisos/${idInstitucion}`)
            .then(response => response.json())
            .then(data => {
                const pisoSelect = document.getElementById(`${tipo ? tipo + '_id_piso' : 'id_piso'}`);
                pisoSelect.innerHTML = '<option value="" disabled selected>Seleccione un piso</option>';
                
                data.pisos.forEach(piso => {
                    const option = document.createElement('option');
                    option.value = piso.id_piso;
                    option.textContent = piso.nombre;
                    pisoSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error al cargar los pisos:', error));
    }
    
