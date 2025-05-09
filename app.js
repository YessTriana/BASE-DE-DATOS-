// Obtener el contenedor de los eventos
const eventosContainer = document.getElementById('eventos-container');

// Función para cargar los eventos desde la API
async function cargarEventos() {
    try {
        const response = await fetch('http://127.0.0.1:5000/eventos'); // Tu endpoint de la API
        const eventos = await response.json();

        // Limpiar el contenedor antes de agregar los nuevos eventos
        eventosContainer.innerHTML = '';

        // Iterar sobre los eventos y crear una tarjeta para cada uno
        eventos.forEach(evento => {
            const card = document.createElement('div');
            card.classList.add('evento-card');

            card.innerHTML = `
                <img src="${evento.imagen_url}" alt="${evento.titulo}">
                <h3>${evento.titulo}</h3>
                <p>${evento.descripcion}</p>
            `;

            // Agregar la tarjeta al contenedor
            eventosContainer.appendChild(card);
        });
    } catch (error) {
        console.error('Error cargando eventos:', error);
        eventosContainer.innerHTML = '<p>No se pudieron cargar los eventos.</p>';
    }
}

// Cargar los eventos al cargar la página
document.addEventListener('DOMContentLoaded', cargarEventos);
