document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");
    const selectedPlayersContainer = document.getElementById("selected-players");
    const comparisonResultsContainer = document.getElementById("comparison-results");
    const selectedPlayers = new Map();
    let radarChart = null; // Instancia del radar chart

    // Generar colores dinámicos basados en índices
    const generateColor = (index) => {
        const hue = (index * 60) % 360; // Cambia el matiz según el índice
        return {
            background: `hsla(${hue}, 70%, 70%, 0.4)`,
            border: `hsla(${hue}, 70%, 70%, 1)`,
            point: `hsla(${hue}, 70%, 40%, 1)`,
        };
    };

    // Buscar jugadores dinámicamente
    searchInput.addEventListener("input", async function () {
        const query = searchInput.value.trim();

        if (!query) {
            searchResults.innerHTML = "<p class='text-muted text-center'>Escribe para buscar jugadores.</p>";
            return;
        }

        try {
            const response = await fetch(`/api/jugadores/?q=${query}`);
            const data = await response.json();
            searchResults.innerHTML = ""; // Limpiar resultados previos

            if (data.jugadores.length === 0) {
                searchResults.innerHTML = "<p class='text-muted text-center'>No se encontraron jugadores.</p>";
                return;
            }

            data.jugadores.forEach((jugador) => {
                const listItem = document.createElement("div");
                listItem.className = "list-group-item d-flex align-items-center justify-content-between p-2 rounded";
                listItem.style.border = "1px solid #ddd";
                listItem.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.1)";
                listItem.innerHTML = `
                    <span class="fw-bold">${jugador.nombre} <small class="text-muted">(${jugador.puesto})</small></span>
                    <button class="btn btn-sm btn-primary add-btn rounded-pill px-3" data-id="${jugador.id}">Añadir</button>
                `;

                const addButton = listItem.querySelector(".add-btn");
                addButton.addEventListener("click", function () {
                    if (!selectedPlayers.has(jugador.id)) {
                        selectedPlayers.set(jugador.id, jugador);
                        renderSelectedPlayers();
                        loadComparison(Array.from(selectedPlayers.keys()));
                    }
                });

                searchResults.appendChild(listItem);
            });
        } catch (error) {
            console.error("Error al buscar jugadores:", error);
        }
    });

    // Limpiar selección
    document.getElementById("clear-selection").addEventListener("click", function () {
        selectedPlayers.clear();
        renderSelectedPlayers();
        comparisonResultsContainer.innerHTML = "<p class='text-muted text-center'>Selecciona jugadores para comparar.</p>";
        if (radarChart) radarChart.destroy(); // Limpia el radar si no hay jugadores
    });

    // Renderizar jugadores seleccionados
    function renderSelectedPlayers() {
        selectedPlayersContainer.innerHTML = "";
        Array.from(selectedPlayers.entries()).forEach(([id, jugador], index) => {
            const colors = generateColor(index); // Colores dinámicos para cada jugador
            const card = document.createElement("div");
            card.className = "card shadow-sm player-card";
            card.style.width = "140px";
            card.style.border = `3px solid ${colors.border}`;
            card.style.backgroundColor = colors.background;

            card.innerHTML = `
                <div class="position-relative text-center">
                    <img src="${jugador.foto || '/static/img/default-player.png'}" class="card-img-top mx-auto d-block" alt="${jugador.nombre}" style="width: 60%;">
                    <button class="btn btn-danger btn-sm position-absolute top-0 end-0 m-2 rounded-circle" data-id="${id}">&times;</button>
                </div>
                <div class="card-body text-center">
                    <h6 class="card-title text-truncate">${jugador.nombre}</h6>
                    <p class="card-text text-muted">${jugador.puesto}</p>
                </div>
            `;

            const removeButton = card.querySelector("button");
            removeButton.addEventListener("click", function () {
                selectedPlayers.delete(parseInt(removeButton.dataset.id));
                renderSelectedPlayers();
                loadComparison(Array.from(selectedPlayers.keys())); // Actualizar tabla
            });

            selectedPlayersContainer.appendChild(card);
        });
    }

    // Cargar comparación dinámica
    async function loadComparison(valoracionesIds) {
        if (valoracionesIds.length === 0) {
            comparisonResultsContainer.innerHTML = "<p class='text-muted text-center'>Selecciona jugadores para comparar.</p>";
            if (radarChart) radarChart.destroy(); // Limpia el radar si no hay jugadores
            return;
        }

        try {
            const response = await fetch(`/api/comparar/?valoraciones=${valoracionesIds.join(",")}`);
            const data = await response.json();

            if (data.jugadores.length === 0) {
                comparisonResultsContainer.innerHTML = "<p class='text-muted text-center'>No se encontraron jugadores para comparar.</p>";
                if (radarChart) radarChart.destroy();
                return;
            }

            // Actualizar la tabla de comparación
            const cualidades = [...new Set(data.jugadores.flatMap(j => j.cualidades.map(c => c.nombre)))];
            let tableHTML = `
                <table class="table table-bordered text-center">
                    <thead class="table-dark">
                        <tr>
                            <th class="fw-bold">Cualidad</th>
                            ${data.jugadores.map(j => `<th>${j.nombre}</th>`).join("")}
                        </tr>
                    </thead>
                    <tbody>
            `;

            cualidades.forEach(cualidad => {
                const valores = data.jugadores.map(j => j.cualidades.find(c => c.nombre === cualidad)?.valor || 0);
                const maxValor = Math.max(...valores);
                const minValor = Math.min(...valores);

                tableHTML += `<tr><td class="fw-bold">${cualidad}</td>`;
                valores.forEach(valor => {
                    const color = valor === maxValor ? "table-success" : valor === minValor ? "table-danger" : "";
                    tableHTML += `<td class="${color}">${valor}</td>`;
                });
                tableHTML += `</tr>`;
            });

            tableHTML += "</tbody></table>";
            comparisonResultsContainer.innerHTML = tableHTML;

            // Actualizar el radar chart con las estadísticas dinámicas
            const radarData = data.jugadores.map((jugador, index) => {
                const colors = generateColor(index); // Colores dinámicos para cada jugador
                return {
                    label: jugador.nombre,
                    data: cualidades.map(cualidad => jugador.cualidades.find(c => c.nombre === cualidad)?.valor || 0),
                    backgroundColor: colors.background,
                    borderColor: colors.border,
                    pointBackgroundColor: colors.point,
                };
            });

            updateRadarChart(cualidades, radarData);
        } catch (error) {
            console.error("Error al cargar la comparación:", error);
        }
    }

    // Actualizar el radar chart
    function updateRadarChart(labels, jugadoresData) {
        if (radarChart) radarChart.destroy(); // Destruir gráfico previo

        const ctx = document.getElementById("player-radar").getContext("2d");
        radarChart = new Chart(ctx, {
            type: "radar",
            data: {
                labels: labels,
                datasets: jugadoresData,
            },
            options: {
                responsive: true,
                maintainAspectRatio: true, // Ajustar el gráfico al contenedor
                plugins: {
                    legend: {
                        display: true,
                        position: "top",
                    },
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            backdropColor: "transparent",
                            stepSize: 20,
                            color: "gray",
                        },
                        grid: {
                            color: "rgba(0, 0, 0, 0.2)",
                        },
                        angleLines: {
                            color: "rgba(0, 0, 0, 0.3)",
                        },
                    },
                },
            },
        });
    }
});
