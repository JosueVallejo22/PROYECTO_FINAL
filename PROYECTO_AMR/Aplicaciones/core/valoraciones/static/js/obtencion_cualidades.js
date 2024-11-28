// Obtiene los valores actuales ingresados en las estadísticas
function obtenerValoresEstadisticas() {
    const valores = {};
    document.querySelectorAll('.estadistica-input').forEach(input => {
        const estadisticaNombre = input.name.replace("estadistica_", ""); // Usar nombre descriptivo
        const valor = parseFloat(input.value) || 0;
        valores[estadisticaNombre] = valor;
    });
    return valores;
}

// Validar el formulario dinámicamente
function validarFormulario() {
    const guardarBtn = document.getElementById("guardar-btn");
    const jugadorSeleccionado = document.getElementById("jugador").value;
    const estadisticasCompletas = Array.from(document.querySelectorAll('.estadistica-input')).every(input => input.value.trim() !== '');
    const cualidadesCalculadas = Array.from(document.querySelectorAll('#calculos-container input')).every(input => input.value.trim() !== '' && input.value.trim() !== 'N/A');

    // Habilitar el botón solo si se cumplen todas las condiciones
    guardarBtn.disabled = !(jugadorSeleccionado && estadisticasCompletas && cualidadesCalculadas);
}

// Cargar cualidades y estadísticas al cambiar el jugador
document.getElementById("jugador").addEventListener("change", function () {
    const jugadorId = this.value;
    const puestoInput = document.getElementById("puesto");
    const calculosContainer = document.getElementById("calculos-container");
    const acordeon = document.getElementById("accordionEstadisticas");
    const guardarBtn = document.getElementById("guardar-btn");

    // Limpiar contenido anterior y deshabilitar el botón
    puestoInput.value = '';
    calculosContainer.innerHTML = `
        <div class="d-flex justify-content-center align-items-center">
            <div class="spinner-border text-dark" role="status"></div>
            <span class="ms-2 text-dark fw-bold">Cargando datos...</span>
        </div>`;
    acordeon.innerHTML = `
        <div class="d-flex justify-content-center align-items-center">
            <div class="spinner-border text-dark" role="status"></div>
            <span class="ms-2 text-dark fw-bold">Cargando estadísticas...</span>
        </div>`;
    guardarBtn.disabled = true;

    // Verificar si se seleccionó un jugador
    if (jugadorId) {
        fetch(`/cargar-cualidades/${jugadorId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error en la respuesta del servidor");
                return response.json();
            })
            .then(data => {
                // Procesar y cargar las cualidades
                puestoInput.value = data.puesto || "Sin puesto asignado";
                calculosContainer.innerHTML = '';
                acordeon.innerHTML = '';

                if (data.cualidades && data.cualidades.length > 0) {
                    data.cualidades.forEach((cualidad, index) => {
                        const cualidadHTML = `
                            <div class="col-md-2 mb-3">
                                <label class="form-label fw-bold text-dark">${cualidad.cualidad}</label>
                                <input type="text" class="form-control border-dark text-dark fw-bold shadow-sm" readonly id="calculo_${cualidad.cualidad}" name="calculo_${cualidad.cualidad.toUpperCase()}" value="0">
                            </div>`;
                        calculosContainer.insertAdjacentHTML("beforeend", cualidadHTML);

                        const estadisticasHTML = cualidad.estadisticas.map((estadistica, idx) => `
                            <tr>
                                <td class="text-center fw-bold">${idx + 1}</td>
                                <td class="text-muted">
                                    ${estadistica.nombre}
                                    <small class="d-block text-secondary fst-italic">${estadistica.descripcion}</small> <!-- Mostrar descripción -->
                                </td>
                                <td>
                                    <input type="number" name="estadistica_${estadistica.nombre}" class="form-control estadistica-input">
                                </td>
                            </tr>`).join("");

                        const acordeonHTML = `
                            <div class="accordion-item border-dark">
                                <h2 class="accordion-header" id="heading${index}">
                                    <button class="accordion-button collapsed text-dark fw-bold shadow-sm" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                                        ${cualidad.cualidad}
                                    </button>
                                </h2>
                                <div id="collapse${index}" class="accordion-collapse collapse" data-bs-parent="#accordionEstadisticas">
                                    <div class="accordion-body bg-light">
                                        <table class="table table-striped table-hover border">
                                            <tbody>${estadisticasHTML}</tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>`;
                        acordeon.insertAdjacentHTML("beforeend", acordeonHTML);
                    });

                    // Agregar validación a los campos recién generados
                    document.querySelectorAll(".estadistica-input").forEach(input => {
                        input.addEventListener("input", () => {
                            validarFormulario(); // Validar formulario al ingresar valores
                        });
                    });
                } else {
                    calculosContainer.innerHTML = `
                        <p class="text-center text-danger fw-bold">No hay cálculos disponibles para este jugador.</p>`;
                    guardarBtn.disabled = true;
                }

                // Revalidar el formulario al cargar los datos
                validarFormulario();
            })
            .catch(error => {
                console.error("Error al cargar datos:", error);
                puestoInput.value = "Error al cargar datos";
                calculosContainer.innerHTML = `
                    <p class="text-center text-danger fw-bold">Error al cargar cualidades.</p>`;
                acordeon.innerHTML = `
                    <p class="text-center text-danger fw-bold">Error al cargar estadísticas.</p>`;
                guardarBtn.disabled = true;
            });
    } else {
        // Mostrar mensaje si no se selecciona un jugador
        calculosContainer.innerHTML = `
            <p class="text-center text-muted fw-bold">Seleccione un jugador para ver los cálculos.</p>`;
        acordeon.innerHTML = `
            <p class="text-center text-muted fw-bold">Seleccione un jugador para cargar las estadísticas.</p>`;
        guardarBtn.disabled = true;
    }

    // Validar formulario después de cambio
    validarFormulario();
});
