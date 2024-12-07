
function openEliminarModal(idOpinion) {
    document.getElementById('delete_id_opinion').value = idOpinion; // Cambiado a idOpinion
    document.getElementById('eliminarOpinionModal').style.display = 'block'; // Cambiado a eliminarOpinionModal
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}



