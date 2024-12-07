
function toggleDropdown() {
    var dropdown = document.getElementById("dropdown-content");
    dropdown.classList.toggle("show");
}

function mostrarUbicaciones() {
    if (!calefactores || !Array.isArray(calefactores) || calefactores.length === 0) {
        console.error("No hay calefactores disponibles.");
        return;
    }

    const planoContainer = document.getElementById("plano-container");

    calefactores.forEach(calefactor => {
        const { coordenadas, estado, id_calefactor } = calefactor;

        // Hacer una solicitud para obtener el nombre de la ubicación
        fetch(`/ubicacion/info/${id_calefactor}`)
            .then(response => response.json())
            .then(data => {
                const nombreUbicacion = data.nombre_ubicacion || 'Desconocido';
                
                if (!coordenadas) {
                    console.warn(`El calefactor con ID ${id_calefactor} no tiene coordenadas.`);
                    return;
                }

                const [x, y] = coordenadas.split(',').map(coord => parseFloat(coord));

                const marcador = document.createElement('div');
                marcador.classList.add('ubicacion-marcador', estado === 'encendido' ? 'encendido' : 'apagado');
                marcador.style.left = `${x}px`;
                marcador.style.top = `${y}px`;

                // Crear tooltip con el nombre de la ubicación y el estado del calefactor
                const tooltip = document.createElement('div');
                tooltip.classList.add('tooltip');
                tooltip.textContent = `${nombreUbicacion} - ${estado}`;
                document.body.appendChild(tooltip);

                // Eventos para mostrar y ocultar el tooltip
                marcador.addEventListener('mouseover', (e) => {
                    tooltip.style.opacity = 1;
                    tooltip.style.left = `${e.pageX + 10}px`;
                    tooltip.style.top = `${e.pageY + 10}px`;
                });

                marcador.addEventListener('mousemove', (e) => {
                    tooltip.style.left = `${e.pageX + 10}px`;
                    tooltip.style.top = `${e.pageY + 10}px`;
                });

                marcador.addEventListener('mouseout', () => {
                    tooltip.style.opacity = 0;
                });

                // Evento de clic para abrir el modal
                marcador.onclick = () => mostrarInformacion(id_calefactor);

                planoContainer.appendChild(marcador);
            })
            .catch(error => console.error('Error al obtener la información de la ubicación:', error));
    });
}



function mostrarInformacion(id_calefactor) {
    fetch(`/ubicacion/info/${id_calefactor}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener la información de la ubicación.');
            }
            return response.json();
        })
        .then(data => {
            // Actualiza el contenido del modal con los datos obtenidos
            document.getElementById('imagen-ubicacion').src = `/static/img/uploads/${data.imagen_ubicacion.split('/').pop()}`;
            document.getElementById('temperatura-ubicacion').textContent = data.ultima_temperatura || 'No disponible';

            abrirModal();  // Abre el modal con la información
        })
        .catch(error => console.error('Error al obtener los datos de la ubicación:', error));
}

function abrirModal() {
    const modal = document.getElementById('informacionModal');
    modal.style.display = 'block';
}

function cerrarModal() {
    const modal = document.getElementById('informacionModal');
    modal.style.display = 'none';
}

