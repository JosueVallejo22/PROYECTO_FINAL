document.addEventListener("DOMContentLoaded", function () {
    // Elementos DOM
    const jugadorSelect = document.getElementById("jugador-select");
    const arqueroSelect = document.getElementById("arquero-select");
    const evolucionInfo = document.getElementById("evolucion-info");
    const distribucionInfo = document.getElementById("distribucion-info");
    const penalesInfo = document.getElementById("penales-info");
    const distribucionListadoMinimal = document.getElementById("distribucion-listado-minimal");

    // Gráficos
    const evolucionCtx = document.getElementById("evolucionChart").getContext("2d");
    const distribucionCtx = document.getElementById("distribucionChart").getContext("2d");
    const penalesCtx = document.getElementById("penalesChart").getContext("2d");

    // Colores para los gráficos
    const colors = [
        "rgba(75, 192, 192, 1)",
        "rgba(255, 99, 132, 1)",
        "rgba(54, 162, 235, 1)",
        "rgba(255, 206, 86, 1)",
        "rgba(153, 102, 255, 1)",
        "rgba(255, 159, 64, 1)",
    ];
    const backgroundColors = colors.map((color) => color.replace("1)", "0.2)"));

    // Inicialización de gráficos
    let evolucionChart = new Chart(evolucionCtx, {
        type: "line",
        data: {
            labels: [],
            datasets: [],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
            },
            scales: {
                x: { title: { display: true, text: "Fechas" } },
                y: { title: { display: true, text: "Valoración Total" }, beginAtZero: true },
            },
        },
    });

    let distribucionChart = new Chart(distribucionCtx, {
        type: "doughnut",
        data: {
            labels: [],
            datasets: [
                {
                    data: [],
                    backgroundColor: backgroundColors,
                    borderColor: colors,
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
            },
        },
    });

    let penalesChart = new Chart(penalesCtx, {
        type: "bar",
        data: {
            labels: [], // Nombres de los arqueros
            datasets: [
                {
                    label: "Penales Atajados",
                    data: [], // Penales atajados
                    backgroundColor: "rgba(75, 192, 192, 0.8)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1,
                },
                {
                    label: "Penales No Atajados",
                    data: [], // Penales no atajados (calculados como recibidos - atajados)
                    backgroundColor: "rgba(255, 0, 0, 0.8)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
            },
            scales: {
                x: { title: { display: true, text: "Arqueros" }, stacked: true },
                y: {
                    title: { display: true, text: "Penales" },
                    beginAtZero: true,
                    stacked: true,
                },
            },
        },
    });

    // Función para cargar datos de evolución de un jugador
    async function cargarEvolucion(jugadorId) {
        try {
            const response = await fetch(`/dashboards/${jugadorId}/evolucion-data/`);
            const data = await response.json();

            // Limpiar el gráfico actual
            evolucionChart.data.labels = [];
            evolucionChart.data.datasets = [];

            const colorIndex = 0;

            // Agregar fechas al eje X
            evolucionChart.data.labels = data.fechas;

            // Crear dataset para el jugador
            evolucionChart.data.datasets.push({
                label: `Evolución de ${data.jugador}`,
                data: data.valoraciones_totales,
                borderColor: colors[colorIndex],
                backgroundColor: backgroundColors[colorIndex],
                pointRadius: 4,
                tension: 0.3,
                fill: true,
            });

            evolucionChart.update();
            evolucionInfo.textContent = `Mostrando evolución de ${data.jugador}.`;
        } catch (error) {
            console.error("Error al cargar evolución:", error);
        }
    }

    // Función para cargar datos de distribución de jugadores
    async function cargarDistribucion() {
        try {
            const response = await fetch(`/dashboards/distribucion/`);
            const data = await response.json();

            // Actualizar datos del gráfico
            distribucionChart.data.labels = data.puestos.map((p) => p.puesto);
            distribucionChart.data.datasets[0].data = data.puestos.map((p) => p.total_jugadores);
            distribucionChart.update();

            // Actualizar el listado minimalista
            distribucionListadoMinimal.innerHTML = "";
            data.puestos.forEach((p, index) => {
                const badge = document.createElement("span");
                badge.className = `badge bg-${index % 2 === 0 ? "info" : "secondary"} m-1`;
                badge.innerText = `${p.puesto}: ${p.total_jugadores}`;
                distribucionListadoMinimal.appendChild(badge);
            });

            distribucionInfo.textContent = "Distribución actualizada.";
        } catch (error) {
            console.error("Error al cargar distribución:", error);
        }
    }

    // Función para cargar datos de penales atajados
    async function cargarPenales(jugadorId = null) {
        try {
            const url = jugadorId ? `/dashboards/penales/${jugadorId}/` : `/dashboards/penales/`;
            const response = await fetch(url);
            const data = await response.json();

            // Actualizar datos del gráfico
            penalesChart.data.labels = data.jugadores.map((j) => j.nombre);
            penalesChart.data.datasets[0].data = data.jugadores.map((j) => j.penales_atajados);
            penalesChart.data.datasets[1].data = data.jugadores.map(
                (j) => j.penales_recibidos - j.penales_atajados
            );
            penalesChart.update();

            penalesInfo.textContent = jugadorId
                ? `Mostrando datos de penales para ${data.jugadores[0]?.nombre}.`
                : "Mostrando datos de penales para todos los arqueros.";
        } catch (error) {
            console.error("Error al cargar datos de penales:", error);
        }
    }

    // Eventos
    jugadorSelect.addEventListener("change", function () {
        const jugadorId = this.value;
        if (jugadorId) cargarEvolucion(jugadorId);
    });

    arqueroSelect.addEventListener("change", function () {
        const arqueroId = this.value;
        cargarPenales(arqueroId || null);
    });

    // Cargar datos iniciales
    cargarDistribucion();
    cargarPenales();
});
