document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");
    const selectedPlayersContainer = document.getElementById("selected-players");
    const comparisonResultsContainer = document.getElementById("comparison-results");
    const selectedPlayers = new Map(); // Valoración ID -> {nombre, puesto, foto}

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
                listItem.className = "list-group-item d-flex align-items-center justify-content-between";
                listItem.innerHTML = `
                    <span>${jugador.nombre} (${jugador.puesto})</span>
                    <button class="btn btn-sm btn-primary add-btn" data-id="${jugador.id}">
                        Añadir
                    </button>
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
    });

    // Añadir selección (opcional si decides añadir todos los jugadores seleccionados de golpe)
    document.getElementById("add-selection").addEventListener("click", function () {
        renderSelectedPlayers();
        loadComparison(Array.from(selectedPlayers.keys()));
    });

    // Renderizar jugadores seleccionados
    function renderSelectedPlayers() {
        selectedPlayersContainer.innerHTML = "";
        selectedPlayers.forEach((jugador, id) => {
            const card = document.createElement("div");
            card.className = "card shadow-sm";
            card.style.width = "160px";
            card.innerHTML = `
                <div class="position-relative">
                    <img src="${jugador.foto || '/static/img/default-player.png'}" class="card-img-top rounded" alt="${jugador.nombre}">
                    <button class="btn btn-danger btn-sm position-absolute top-0 end-0 m-2" data-id="${id}">
                        &times;
                    </button>
                </div>
                <div class="card-body text-center">
                    <h6 class="card-title">${jugador.nombre}</h6>
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
            return;
        }

        try {
            const response = await fetch(`/api/comparar/?valoraciones=${valoracionesIds.join(",")}`);
            const data = await response.json();

            if (data.jugadores.length === 0) {
                comparisonResultsContainer.innerHTML = "<p class='text-muted text-center'>No se encontraron jugadores para comparar.</p>";
                return;
            }

            const cualidades = [...new Set(data.jugadores.flatMap(j => j.cualidades.map(c => c.nombre)))];
            let tableHTML = `
                <table class="table table-bordered text-center">
                    <thead class="table-dark">
                        <tr>
                            <th>Cualidad</th>
                            ${data.jugadores.map(j => `<th>${j.nombre}</th>`).join("")}
                        </tr>
                    </thead>
                    <tbody>
            `;

            cualidades.forEach((cualidad) => {
                const valores = data.jugadores.map((j) =>
                    j.cualidades.find((c) => c.nombre === cualidad)?.valor || 0
                );
                const maxValor = Math.max(...valores);
                const minValor = Math.min(...valores);

                tableHTML += `<tr><td>${cualidad}</td>`;
                valores.forEach((valor) => {
                    const color = valor === maxValor ? "table-success" : valor === minValor ? "table-danger" : "";
                    tableHTML += `<td class="${color}">${valor}</td>`;
                });
                tableHTML += `</tr>`;
            });

            tableHTML += "</tbody></table>";
            comparisonResultsContainer.innerHTML = tableHTML;
        } catch (error) {
            console.error("Error al cargar la comparación:", error);
        }
    }
});
