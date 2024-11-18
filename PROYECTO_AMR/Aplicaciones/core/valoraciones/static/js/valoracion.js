document.addEventListener("DOMContentLoaded", function () {
    // Configurar la fecha y hora actual
    const fechaInput = document.getElementById("fecha");
    const horaInput = document.getElementById("hora");

    const ahora = new Date();
    const fechaActual = ahora.toLocaleDateString("es-ES", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
    }); // Formato: dd/mm/yyyy

    const horaActual = ahora.toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    }); // Formato: hh:mm:ss

    fechaInput.value = fechaActual; // Establecer la fecha actual
    horaInput.value = horaActual; // Establecer la hora actual
});

// Manejar cambios al seleccionar un jugador
document.getElementById("jugador").addEventListener("change", function () {
    const jugadorId = this.value;
    const puestoInput = document.getElementById("puesto");
    const cualidadesContainer = document.getElementById("cualidades-container");
    const acordeon = document.getElementById("accordionEstadisticas");
    const guardarBtn = document.getElementById("guardar-btn");

    if (jugadorId) {
        fetch(`/cargar-cualidades/${jugadorId}/`)
            .then(response => response.json())
            .then(data => {
                // Limpiar campos
                puestoInput.value = data.puesto || "Sin puesto asignado";
                cualidadesContainer.innerHTML = '';
                acordeon.innerHTML = '';

                // Mostrar cualidades y estadísticas en acordeón
                if (data.cualidades && data.cualidades.length > 0) {
                    data.cualidades.forEach((cualidad, index) => {
                        // Cualidades en la cabecera
                        const col = document.createElement("div");
                        col.className = "col-md-2 mb-3";
                        col.innerHTML = `
                            <label class="form-label">${cualidad.cualidad}</label>
                            <input type="text" class="form-control" placeholder="Calculado automáticamente" readonly>
                        `;
                        cualidadesContainer.appendChild(col);

                        // Estadísticas en acordeón
                        const card = document.createElement("div");
                        card.className = "accordion-item";
                        card.innerHTML = `
                            <h2 class="accordion-header" id="heading${index}">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}">
                                    ${cualidad.cualidad}
                                </button>
                            </h2>
                            <div id="collapse${index}" class="accordion-collapse collapse" aria-labelledby="heading${index}" data-bs-parent="#accordionEstadisticas">
                                <div class="accordion-body">
                                    <table class="table table-bordered text-center">
                                        <thead>
                                            <tr>
                                                <th>#</th>
                                                <th>Estadística</th>
                                                <th>Valor</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${cualidad.estadisticas
                                                .map(
                                                    (estadistica, statIndex) => `
                                                    <tr>
                                                        <td>${statIndex + 1}</td>
                                                        <td>${estadistica.nombre}</td>
                                                        <td><input type="number" name="estadistica_${estadistica.nombre}" class="form-control estadistica-input" placeholder="Ingresar valor"></td>
                                                    </tr>
                                                `
                                                )
                                                .join("")}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        `;
                        acordeon.appendChild(card);
                    });

                    guardarBtn.disabled = false; // Habilitar botón
                } else {
                    cualidadesContainer.innerHTML = '<p class="text-center">Este jugador no tiene cualidades asociadas.</p>';
                    acordeon.innerHTML = '<p class="text-center">No hay estadísticas disponibles para este jugador.</p>';
                    guardarBtn.disabled = true; // Deshabilitar botón
                }
            })
            .catch(error => {
                console.error("Error al cargar datos:", error);
                puestoInput.value = "Error al cargar datos";
                cualidadesContainer.innerHTML = '<p class="text-center text-danger">Error al cargar cualidades.</p>';
                acordeon.innerHTML = '<p class="text-center text-danger">Error al cargar estadísticas.</p>';
                guardarBtn.disabled = true;
            });
    } else {
        // Limpiar todo si no hay jugador seleccionado
        puestoInput.value = "";
        cualidadesContainer.innerHTML = '<p class="text-center">Seleccione un jugador para ver sus cualidades.</p>';
        acordeon.innerHTML = '<p class="text-center">Seleccione un jugador.</p>';
        guardarBtn.disabled = true;
    }
});
