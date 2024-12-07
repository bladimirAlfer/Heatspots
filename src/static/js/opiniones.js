document.addEventListener('DOMContentLoaded', () => {
    const opinionesContainer = document.getElementById('opinionesContainer');
    const currentUserId = parseInt(opinionesContainer.dataset.currentUserId, 10);

    const ratingStars = document.querySelectorAll('.rating-stars .star');
    const opinionList = document.getElementById('opinionesList');
    const opinionText = document.getElementById('opinionText');
    const submitOpinion = document.getElementById('submitOpinion');

    let currentRating = 0;

    // Manejar la calificación dinámica
    ratingStars.forEach(star => {
        star.addEventListener('click', () => {
            currentRating = parseInt(star.dataset.value);
            ratingStars.forEach(s => s.classList.remove('active'));
            for (let i = 0; i < currentRating; i++) {
                ratingStars[i].classList.add('active');
            }
        });
    });

    // Enviar una nueva opinión
    submitOpinion.addEventListener('click', async () => {
        const opinion = opinionText.value.trim();
        if (!opinion || currentRating === 0) {
            alert('Por favor, escribe tu opinión y selecciona una calificación.');
            return;
        }

        const response = await fetch('/api/opiniones', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ opinion, rating: currentRating })
        });

        if (response.ok) {
            alert('Opinión enviada exitosamente.');
            opinionText.value = '';
            currentRating = 0;
            ratingStars.forEach(s => s.classList.remove('active'));
            loadOpinions();
        } else {
            alert('Error al enviar la opinión.');
        }
    });

    // Cargar opiniones
    async function loadOpinions() {
        const response = await fetch('/api/opiniones');
        if (response.ok) {
            const opiniones = await response.json();
    
            opinionList.innerHTML = '';
            opiniones.forEach(o => {
                const card = document.createElement('div');
                card.className = 'opinion-card';
                card.innerHTML = `
                    <div class="user-info">
                        <span>${o.user_name || 'Usuario Anónimo'}</span>
                    </div>
                    <div class="date">${new Date(o.created_at).toLocaleString()}</div>
                    <p>${o.opinion_text}</p>
                    <p>${'★'.repeat(o.rating)}</p>
                    ${
                        currentUserId === o.id_usuario
                            ? `<button class="delete-btn" data-id="${o.id_opinion}">Eliminar</button>`
                            : ''
                    }
                `;
                opinionList.appendChild(card);
            });
            
            
    
            // Manejar eliminación
            document.querySelectorAll('.delete-btn').forEach(btn => {
                btn.addEventListener('click', async () => {
                    const id = btn.dataset.id;
                    const res = await fetch(`/api/opiniones/${id}`, { method: 'DELETE' });
                    if (res.ok) loadOpinions();
                    else alert('Error al eliminar la opinión.');
                });
            });
        } else {
            alert('Error al cargar las opiniones.');
        }
    }
    

    loadOpinions();
});

function toggleDropdown() {
    var dropdown = document.getElementById("dropdown-content");
    dropdown.classList.toggle("show");
}

