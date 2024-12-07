document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('opinionesContainer');
    let currentSlide = 0;

    async function loadOpinions() {
        try {
            const response = await fetch('/api/opiniones');
            if (response.ok) {
                const opiniones = await response.json();
                track.innerHTML = ''; // Limpiar antes de cargar nuevas opiniones

                opiniones.forEach(opinion => {
                    const card = document.createElement('div');
                    card.className = 'opinion-card';
                    card.innerHTML = `
                        <p class="user-name">${opinion.user_name || 'Usuario Anónimo'}</p>
                        <p class="rating">${'★'.repeat(opinion.rating)}</p>
                        <p class="text">${opinion.opinion_text}</p>
                    `;
                    track.appendChild(card);
                });

                // Si hay menos opiniones que el ancho visible, centra el track
                if (opiniones.length < 3) {
                    track.style.justifyContent = 'center';
                }
            } else {
                console.error('Error al cargar las opiniones.');
            }
        } catch (error) {
            console.error('Error al cargar las opiniones:', error);
        }
    }

    function moveCarousel(direction) {
        const slides = track.children;
        const slideWidth = slides[0]?.getBoundingClientRect().width || 0;

        if (!slideWidth) return; // Evita errores si no hay elementos

        currentSlide += direction;

        if (currentSlide < 0) {
            currentSlide = slides.length - 1;
        } else if (currentSlide >= slides.length) {
            currentSlide = 0;
        }

        track.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
    }

    document.querySelector('.carousel-button.prev').addEventListener('click', () => moveCarousel(-1));
    document.querySelector('.carousel-button.next').addEventListener('click', () => moveCarousel(1));

    loadOpinions();
});
