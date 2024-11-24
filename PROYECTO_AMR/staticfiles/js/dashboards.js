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
            labels: [], // Se llenará dinámicamente
            datasets: [], // Se llenará dinámicamente
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false, // Mostrar leyenda
                    labels: {
                        color: "#fff", // Color del texto de la leyenda
                        font: {
                            size: 14, // Tamaño de fuente
                            family: "Arial, sans-serif", // Familia de fuente
                        },
                    },
                },
                tooltip: {
                    backgroundColor: "rgba(0,0,0,0.8)", // Fondo del tooltip
                    titleColor: "#ffc107", // Color del título
                    bodyColor: "#fff", // Color del texto
                    borderColor: "#ffc107", // Borde
                    borderWidth: 1,
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Fechas",
                        color: "#ffc107", // Color del título
                        font: {
                            size: 16,
                            weight: "bold",
                        },
                    },
                    grid: {
                        color: "rgba(255,255,255,0.2)", // Líneas de la cuadrícula
                        borderColor: "#ffc107", // Color del borde del eje
                    },
                    ticks: {
                        color: "#fff", // Color de las etiquetas del eje
                        font: {
                            size: 12,
                        },
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: "Valoración Total",
                        color: "#ffc107",
                        font: {
                            size: 16,
                            weight: "bold",
                        },
                    },
                    beginAtZero: true,
                    grid: {
                        color: "rgba(255,255,255,0.2)",
                        borderColor: "#ffc107",
                    },
                    ticks: {
                        color: "#fff",
                        font: {
                            size: 12,
                        },
                    },
                },
            },
            elements: {
                line: {
                    tension: 0.4, // Curvatura de la línea
                    borderWidth: 2, // Ancho de la línea
                    borderColor: "rgba(75, 192, 192, 1)", // Color de la línea por defecto
                    backgroundColor: "rgba(75, 192, 192, 0.2)", // Color de relleno
                },
                point: {
                    radius: 5, // Radio de los puntos
                    hoverRadius: 7, // Radio al pasar el ratón
                    backgroundColor: "#ffc107", // Color de los puntos
                    borderWidth: 2, // Borde de los puntos
                },
            },
        },
    });
    

    let distribucionChart = new Chart(distribucionCtx, {
        type: "doughnut",
        data: {
            labels: [],
            datasets: [
                {
                    data: [], // Ejemplo de datos
                    backgroundColor: backgroundColors,
                    borderColor: colors,
                    borderWidth: 2,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "bottom",
                    labels: {
                        color: "#ffc107", // Color de las etiquetas de la leyenda
                        font: {
                            size: 14,
                        },
                        boxWidth: 20, // Tamaño del cuadro de color
                        padding: 15, // Espaciado entre elementos de la leyenda
                    },
                },
                tooltip: {
                    backgroundColor: "rgba(0, 0, 0, 0.8)", // Fondo oscuro
                    titleColor: "#ffc107", // Color del título del tooltip
                    bodyColor: "#fff", // Color del texto
                    borderColor: "#ffc107", // Borde del tooltip
                    borderWidth: 1,
                },
            },
            layout: {
                padding: {
                    top: 10,
                    bottom: 0,
                },
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
                    backgroundColor: "rgba(0, 255, 0, 0.8)", // Verde brillante
                    borderColor: "rgba(0, 200, 0, 1)", // Verde más oscuro
                    borderWidth: 2,
                    hoverBackgroundColor: "rgba(0, 255, 0, 1)", // Color al pasar el mouse
                    hoverBorderColor: "#fff", // Borde blanco al hacer hover
                },
                {
                    label: "Penales No Atajados",
                    data: [], // Penales no atajados
                    backgroundColor: "rgba(255, 0, 0, 0.8)", // Rojo brillante
                    borderColor: "rgba(200, 0, 0, 1)", // Rojo más oscuro
                    borderWidth: 2,
                    hoverBackgroundColor: "rgba(255, 0, 0, 1)", // Color al pasar el mouse
                    hoverBorderColor: "#fff", // Borde blanco al hacer hover
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "top", // Leyenda en la parte superior
                    labels: {
                        color: "#fff", // Color del texto de la leyenda
                        font: {
                            size: 14, // Tamaño de la fuente
                            family: "Arial, sans-serif", // Familia de fuente
                        },
                        padding: 15, // Espaciado entre elementos de la leyenda
                    },
                },
                tooltip: {
                    backgroundColor: "rgba(0, 0, 0, 0.8)", // Fondo oscuro
                    titleColor: "#ffc107", // Color del título del tooltip
                    bodyColor: "#fff", // Color del texto
                    borderColor: "#ffc107", // Borde del tooltip
                    borderWidth: 1,
                    padding: 10, // Espaciado interno
                    caretPadding: 10, // Espaciado entre el tooltip y la barra
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Arqueros",
                        color: "#ffc107", // Color del título
                        font: {
                            size: 16,
                            weight: "bold",
                        },
                    },
                    stacked: true,
                    ticks: {
                        color: "#fff", // Color de las etiquetas del eje x
                        font: {
                            size: 12,
                        },
                    },
                    grid: {
                        display: false, // Ocultar líneas de la cuadrícula en x
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: "Penales",
                        color: "#ffc107", // Color del título
                        font: {
                            size: 16,
                            weight: "bold",
                        },
                    },
                    beginAtZero: true,
                    stacked: true,
                    ticks: {
                        color: "#fff", // Color de las etiquetas del eje y
                        font: {
                            size: 12,
                        },
                    },
                    grid: {
                        color: "rgba(255, 255, 255, 0.2)", // Líneas de cuadrícula con opacidad
                    },
                },
            },
            animation: {
                duration: 1500, // Duración de la animación
                easing: "easeInOutCubic", // Efecto de animación suave
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
