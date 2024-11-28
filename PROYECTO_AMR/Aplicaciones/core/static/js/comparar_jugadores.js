let jugadorSeleccionado1 = null;
let jugadorSeleccionado2 = null;

// Función para manejar el evento de buscar jugadores
document.getElementById('input-buscar-jugador').addEventListener('input', function () {
    const query = this.value.trim();

    if (query.length < 2) {
        document.getElementById('lista-jugadores').innerHTML = ''; // Limpiar lista si la búsqueda es muy corta
        return;
    }

    fetch(`/api/jugadores/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            actualizarListaJugadores(data.jugadores);
        })
        .catch(error => {
            console.error('Error al buscar jugadores:', error);
        });
});

// Actualizar la lista de jugadores en el modal
function actualizarListaJugadores(jugadores) {
    const lista = document.getElementById('lista-jugadores');
    lista.innerHTML = '';

    if (jugadores.length === 0) {
        lista.innerHTML = '<li class="list-group-item text-center">No se encontraron jugadores</li>';
        return;
    }

    jugadores.forEach(jugador => {
        const li = document.createElement('li');
        li.classList.add('list-group-item', 'd-flex', 'align-items-center', 'justify-content-between');
        li.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="${jugador.foto}" alt="${jugador.nombre}" class="rounded-circle mr-3" width="50">
                <strong>${jugador.nombre}</strong> - ${jugador.puesto}
            </div>
            <button class="btn btn-sm btn-success">Seleccionar</button>
        `;

        li.querySelector('button').addEventListener('click', () => seleccionarJugador(jugador));
        lista.appendChild(li);
    });
}

// Seleccionar un jugador
function seleccionarJugador(jugador) {

    // Validar que no sea el mismo jugador seleccionado
    if ((jugadorSeleccionado1 && jugadorSeleccionado1.id === jugador.id) || 
        (jugadorSeleccionado2 && jugadorSeleccionado2.id === jugador.id)) {
            Swal.fire({
                icon: 'error',
                title: 'Jugador duplicado',
                text: 'No puedes seleccionar al mismo jugador dos veces.',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Aceptar'
            });
            return;
        }

    if (!jugadorSeleccionado1) {
        jugadorSeleccionado1 = jugador;
        renderJugador('jugador-1', jugador);
    } else if (!jugadorSeleccionado2) {
        jugadorSeleccionado2 = jugador;
        renderJugador('jugador-2', jugador);
    } else {
        Swal.fire({
            icon: 'error', // Ícono de error
            title: 'Límite alcanzado',
            text: 'Solo puedes comparar dos jugadores.',
            confirmButtonColor: '#3085d6', // Color del botón
            confirmButtonText: 'Aceptar'
        });        
        return;
    }

    // Cerrar el modal
    $('#modal-buscar-jugador').modal('hide');
}

// Renderizar jugador seleccionado
function renderJugador(idElemento, jugador) {
    const contenedor = document.getElementById(idElemento);
    contenedor.innerHTML = `
        <div class="jugador-card">
            <div class="jugador-imagen">
                <img src="${jugador.foto}" alt="${jugador.nombre}">
            </div>
            <h5 class="text-warning">${jugador.nombre}</h5>
            <p class="text-warning">${jugador.puesto}</p>
            <button class="btn btn-sm btn-danger quitar-boton" onclick="removerJugador(${jugador.id})">QUITAR</button>
        </div>
    `;
}


// Remover jugador seleccionado
function removerJugador(id) {
    if (jugadorSeleccionado1 && jugadorSeleccionado1.id === id) {
        jugadorSeleccionado1 = null;
        document.getElementById('jugador-1').innerHTML = 'Selecciona un jugador';
        document.getElementById('valores-jugador-1').innerHTML = ''; // Limpiar las cualidades
    } else if (jugadorSeleccionado2 && jugadorSeleccionado2.id === id) {
        jugadorSeleccionado2 = null;
        document.getElementById('jugador-2').innerHTML = 'Selecciona un jugador';
        document.getElementById('valores-jugador-2').innerHTML = ''; // Limpiar las cualidades
    }

    // Opcional: destruir el gráfico si no hay jugadores seleccionados
    if (!jugadorSeleccionado1 && !jugadorSeleccionado2 && window.graficoRadar) {
        window.graficoRadar.destroy();
    }
}


// Comparar jugadores
document.getElementById('btn-comparar').addEventListener('click', () => {
    if (!jugadorSeleccionado1 || !jugadorSeleccionado2) {
        Swal.fire({
            icon: 'warning', // Ícono de advertencia
            title: 'Faltan jugadores',
            text: 'Selecciona dos jugadores para comparar.',
            confirmButtonColor: '#f39c12', // Color del botón (naranja para advertencias)
            confirmButtonText: 'Aceptar'
        });
        return;
    }

    fetch(`/api/comparar-jugadores/?jugador1=${jugadorSeleccionado1.id}&jugador2=${jugadorSeleccionado2.id}`)
        .then(response => response.json())
        .then(data => {
            // Renderizar las cualidades de ambos jugadores
            renderCualidades(data.cualidades, data.jugador1, data.jugador2);
            // Generar el gráfico hexagonal
            generarGraficoHexagonal(data.cualidades, data.jugador1, data.jugador2);
        })
        .catch(error => {
            console.error('Error al comparar jugadores:', error);
        });
});

// Renderizar cualidades en el frontend
function renderCualidades(cualidades, jugador1, jugador2) {
    const valoresJugador1 = document.getElementById('valores-jugador-1');
    const valoresJugador2 = document.getElementById('valores-jugador-2');

    // Limpiar contenido previo
    valoresJugador1.innerHTML = '<h6 class="text-light">Cualidades:</h6><ul class="list-unstyled"></ul>';
    valoresJugador2.innerHTML = '<h6 class="text-light">Cualidades:</h6><ul class="list-unstyled"></ul>';

    const ul1 = valoresJugador1.querySelector('ul');
    const ul2 = valoresJugador2.querySelector('ul');

    cualidades.forEach(cualidad => {
        const valor1 = jugador1.valores[cualidad] || 0;
        const valor2 = jugador2.valores[cualidad] || 0;

        const li1 = document.createElement('li');
        const li2 = document.createElement('li');

        // Determinar colores
        if (valor1 > valor2) {
            li1.style.color = 'green';
            li2.style.color = 'red';
        } else if (valor1 < valor2) {
            li1.style.color = 'red';
            li2.style.color = 'green';
        } else {
            li1.style.color = 'yellow';
            li2.style.color = 'yellow';
        }

        // Resaltar valores con <strong>
        li1.innerHTML = `<strong>${cualidad}: ${valor1}</strong>`;
        li2.innerHTML = `<strong>${cualidad}: ${valor2}</strong>`;

        ul1.appendChild(li1);
        ul2.appendChild(li2);
    });
}


// Generar gráfico hexagonal
function generarGraficoHexagonal(cualidades, jugador1, jugador2) {
    const ctx = document.getElementById('grafico-hexagonal').getContext('2d');

    // Destruir gráfico previo si existe
    if (window.graficoRadar) {
        window.graficoRadar.destroy();
    }

    // Crear el nuevo gráfico
    window.graficoRadar = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: cualidades,
            datasets: [
                {
                    label: jugador1.nombre,
                    data: cualidades.map(c => jugador1.valores[c] || 0),
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                },
                {
                    label: jugador2.nombre,
                    data: cualidades.map(c => jugador2.valores[c] || 0),
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    ticks: {
                        beginAtZero: true,
                        color: '#ffffff', // Cambiar el color de los valores numéricos a blanco
                        backdropColor: 'rgba(0, 0, 0, 0.5)', // Fondo detrás de los valores numéricos
                    },
                    grid: {
                        color: '#cccccc', // Líneas de la red más claras
                    },
                    angleLines: {
                        color: '#cccccc', // Líneas angulares más visibles
                    },
                    pointLabels: {
                        color: '#ffff00', // Cambiar las etiquetas de las cualidades a amarillo
                        font: {
                            size: 14, // Tamaño de las etiquetas
                        },
                    },
                },
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff', // Colores de los nombres de los jugadores
                        font: {
                            size: 14, // Tamaño más grande para mejor legibilidad
                        },
                    },
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            const cualidad = tooltipItem.label;
                            const valor = tooltipItem.raw;
                            return `${cualidad}: ${valor}`;
                        },
                    },
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                },
            },
        },         
    });
}
document.getElementById('modal-buscar-jugador').addEventListener('show.bs.modal', function () {
    // Limpiar el campo de búsqueda y la lista de jugadores
    document.getElementById('input-buscar-jugador').value = '';
    document.getElementById('lista-jugadores').innerHTML = '';
});
