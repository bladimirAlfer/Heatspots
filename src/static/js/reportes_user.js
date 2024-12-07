document.addEventListener('DOMContentLoaded', () => {
    const institucionHeader = document.querySelector('#id_institucion-header');
    const pisoHeader = document.querySelector('#id_piso-header');
    const calefactorHeader = document.querySelector('#id_calefactor-header');
    const tipoReporteHeader = document.querySelector('#tipo_reporte-header');
    const tipoReporteDropdown = tipoReporteHeader.nextElementSibling;

    const institucionDropdown = document.getElementById('id_institucion');
    const pisoDropdown = document.getElementById('id_piso');
    const calefactorDropdown = document.getElementById('id_calefactor');

    // Función para alternar visibilidad del dropdown
    function toggleDropdown(header, dropdown) {
        header.addEventListener('click', () => {
            dropdown.classList.toggle('active');
        });

        document.addEventListener('click', (event) => {
            if (!header.contains(event.target) && !dropdown.contains(event.target)) {
                dropdown.classList.remove('active');
            }
        });
    }

    function selectOption(header, dropdown, callback) {
        dropdown.addEventListener('click', (event) => {
            if (event.target.classList.contains('report-dropdown-option')) {
                const value = event.target.getAttribute('data-value');
                const text = event.target.textContent;
    
                if (value) {
                    header.textContent = text;
                    header.setAttribute('data-selected', value);
    
                    // Actualizar el valor del campo oculto
                    const hiddenInput = document.querySelector(`input[name=${header.getAttribute('data-name')}]`);
                    if (hiddenInput) hiddenInput.value = value;
    
                    dropdown.classList.remove('active');
                    if (callback) callback(value);
                }
            }
        });
    }
    
    
    // Función para popular opciones en un dropdown
    function populateDropdown(dropdown, items) {
        dropdown.innerHTML = ''; // Limpiar contenido previo
        items.forEach(item => {
            const option = document.createElement('div');
            option.classList.add('report-dropdown-option');
            option.textContent = item.nombre || item;
            option.setAttribute('data-value', item.id_institucion || item.id_piso || item.id_calefactor || item);
            dropdown.appendChild(option);
        });
    }

    // Cargar instituciones
    fetch('/api/instituciones')
        .then(response => response.json())
        .then(data => populateDropdown(institucionDropdown, data))
        .catch(error => console.error('Error al cargar instituciones:', error));

    // Manejar selección de institución
    toggleDropdown(institucionHeader, institucionDropdown);
    selectOption(institucionHeader, institucionDropdown, (institucionId) => {
        fetch(`/api/pisos/${institucionId}`)
            .then(response => response.json())
            .then(data => populateDropdown(pisoDropdown, data.pisos))
            .catch(error => console.error('Error al cargar pisos:', error));
    });

    // Manejar selección de piso
    toggleDropdown(pisoHeader, pisoDropdown);
    selectOption(pisoHeader, pisoDropdown, (pisoId) => {
        fetch(`/api/calefactores/${pisoId}`)
            .then(response => response.json())
            .then(data => populateDropdown(calefactorDropdown, data))
            .catch(error => console.error('Error al cargar calefactores:', error));
    });

    // Manejar selección de calefactor
    toggleDropdown(calefactorHeader, calefactorDropdown);
    selectOption(calefactorHeader, calefactorDropdown);

    // Manejar dropdown de tipo de reporte
    toggleDropdown(tipoReporteHeader, tipoReporteDropdown);
    selectOption(tipoReporteHeader, tipoReporteDropdown);
});

function toggleDropdown() {
    var dropdown = document.getElementById("dropdown-content");
    dropdown.classList.toggle("show");
}
