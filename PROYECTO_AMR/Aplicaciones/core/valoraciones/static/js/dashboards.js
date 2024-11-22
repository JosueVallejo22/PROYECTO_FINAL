document.addEventListener("DOMContentLoaded", function () {
    const selectContainer = document.getElementById("jugador-select-container");
    const ctx = document.getElementById("jugadorChart").getContext("2d");
    const chartTitle = document.getElementById("chart-title");
    const chartInfo = document.getElementById("chart-info");

    const colors = [
        "rgba(75, 192, 192, 1)",
        "rgba(255, 99, 132, 1)",
        "rgba(54, 162, 235, 1)",
        "rgba(255, 206, 86, 1)",
        "rgba(153, 102, 255, 1)",
        "rgba(255, 159, 64, 1)",
    ];

    const backgroundColors = colors.map((color) => color.replace("1)", "0.2)"));

    let chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [], // Este eje mostrará los índices
            datasets: [],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const datasetIndex = context.datasetIndex;
                            const index = context.dataIndex;
                            const fecha = chart.data.datasets[datasetIndex].fechas[index];
                            const valor = context.raw;
                            return `Valor: ${valor}, Fecha: ${fecha}`;
                        },
                    },
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Valoraciones",
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: "Valoración Total",
                    },
                    beginAtZero: true,
                },
            },
        },
    });

    let selectCount = 1;
    const jugadoresSeleccionados = new Map(); // Rastrea los jugadores seleccionados por ID de selector

    // Función para agregar o actualizar un jugador en el gráfico
    async function agregarJugador(jugadorId, selectElement) {
        try {
            const response = await fetch(`/jugador/${jugadorId}/evolucion-data/`);
            const data = await response.json();

            // Si el jugador ya está en otro selector, evitar duplicados
            if (jugadoresSeleccionados.has(jugadorId) && jugadoresSeleccionados.get(jugadorId) !== selectElement.id) {
                alert("Este jugador ya está seleccionado en otro campo.");
                selectElement.value = ""; // Restablecer el select
                return;
            }

            const selectorId = selectElement.id;

            // Si el selector ya tenía un jugador, eliminarlo del gráfico
            if (jugadoresSeleccionados.has(selectorId)) {
                const jugadorAnteriorId = jugadoresSeleccionados.get(selectorId);
                const datasetIndex = chart.data.datasets.findIndex((ds) => ds.label === jugadorAnteriorId);
                if (datasetIndex !== -1) {
                    chart.data.datasets.splice(datasetIndex, 1);
                }
                jugadoresSeleccionados.delete(jugadorAnteriorId);
            }

            // Agregar el nuevo jugador al gráfico
            const colorIndex = chart.data.datasets.length % colors.length;
            chart.data.datasets.push({
                label: data.jugador,
                data: data.valoraciones_totales,
                borderColor: colors[colorIndex],
                backgroundColor: backgroundColors[colorIndex],
                pointBackgroundColor: colors[colorIndex],
                pointRadius: 4,
                tension: 0.3,
                fill: true,
                fechas: data.fechas,
            });

            // Ajustar etiquetas (índices)
            if (chart.data.labels.length < data.valoraciones_totales.length) {
                chart.data.labels = data.valoraciones_totales.map((_, i) => i + 1); // Índices
            }

            chart.update();
            chartInfo.textContent = `Comparando ${chart.data.datasets.length} jugadores.`;

            jugadoresSeleccionados.set(selectorId, jugadorId); // Actualizar el jugador seleccionado para este selector
        } catch (error) {
            console.error("Error al cargar los datos del jugador:", error);
        }
    }

    // Función para agregar un nuevo selector de jugador
    function agregarNuevoSelector() {
        selectCount++;
        const newSelect = document.createElement("select");
        newSelect.id = `jugador-select-${selectCount}`;
        newSelect.className = "form-select jugador-select mt-2";

        // Agregar opciones excluyendo las ya seleccionadas
        newSelect.innerHTML = `<option value="" disabled selected>-- Selecciona un jugador --</option>`;
        document.querySelectorAll("#jugador-select-1 option").forEach((option) => {
            const jugadorId = option.value;
            if (!Array.from(jugadoresSeleccionados.values()).includes(jugadorId) && jugadorId !== "") {
                newSelect.innerHTML += `<option value="${jugadorId}">${option.textContent}</option>`;
            }
        });

        selectContainer.appendChild(newSelect);

        newSelect.addEventListener("change", function () {
            const jugadorId = this.value;
            if (jugadorId) {
                agregarJugador(jugadorId, newSelect);
            }
        });
    }

    // Evento inicial para el primer selector
    document.getElementById("jugador-select-1").addEventListener("change", function () {
        const jugadorId = this.value;
        if (jugadorId) {
            agregarJugador(jugadorId, this);
        }
    });
});
