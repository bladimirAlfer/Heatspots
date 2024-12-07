function openEliminarModal(email) {
    const modal = document.getElementById('eliminarUsuarioModal');
    const emailInput = document.getElementById('delete_user_email');
    emailInput.value = email;
    modal.style.display = 'block';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('eliminarUsuarioModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};
