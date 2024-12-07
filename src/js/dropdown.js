function toggleDropdown() {
    console.log("Dropdown clicked");  // Para verificar si se hace clic en el botón
    var dropdown = document.getElementById("dropdown-content");
    dropdown.classList.toggle("show");  // Alternar la clase 'show'
}

// Cerrar el dropdown si se hace clic fuera de él
window.onclick = function(event) {
    // Si el clic no fue en el botón del dropdown o dentro del dropdown, lo cerramos
    if (!event.target.matches('.dropdown-toggle') && !event.target.closest('.dropdown-content')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');  // Remover la clase 'show'
            }
        }
    }
}
