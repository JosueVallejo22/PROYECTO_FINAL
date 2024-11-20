// Obtiene los valores actuales ingresados en las estadísticas
function obtenerValoresEstadisticas() {
    const valores = {};
    document.querySelectorAll('.estadistica-input').forEach(input => {
        const estadisticaNombre = input.name.replace("estadistica_", "");
        const valor = parseFloat(input.value) || 0;
        valores[estadisticaNombre] = valor;
    });
    return valores;
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
    calculosContainer.innerHTML = '<p class="text-center">Cargando datos...</p>';
    acordeon.innerHTML = '<p class="text-center">Cargando estadísticas...</p>';
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
                                <label class="form-label">${cualidad.cualidad}</label>
                                <input type="text" class="form-control" readonly id="calculo_${cualidad.cualidad}">
                            </div>`;
                        calculosContainer.insertAdjacentHTML("beforeend", cualidadHTML);

                        const estadisticasHTML = cualidad.estadisticas.map((estadistica, idx) => `
                            <tr>
                                <td>${idx + 1}</td>
                                <td>${estadistica.nombre}</td>
                                <td>
                                    <input type="number" name="estadistica_${estadistica.nombre}" class="form-control estadistica-input">
                                </td>
                            </tr>`).join("");

                        const acordeonHTML = `
                            <div class="accordion-item">
                                <h2 class="accordion-header" id="heading${index}">
                                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                                        ${cualidad.cualidad}
                                    </button>
                                </h2>
                                <div id="collapse${index}" class="accordion-collapse collapse">
                                    <div class="accordion-body">
                                        <table class="table">
                                            <tbody>${estadisticasHTML}</tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>`;
                        acordeon.insertAdjacentHTML("beforeend", acordeonHTML);
                    });

                    // Rehabilitar el botón de guardar si no hay errores
                    guardarBtn.disabled = false;

                    // Revalidar los campos recién generados
                    document.querySelectorAll(".estadistica-input").forEach(input => {
                        input.addEventListener("input", () => {
                            if (typeof validarCampo === 'function') {
                                validarCampo(input); // Validación dinámica
                            }
                        });
                    });

                    // Validar globalmente el formulario
                    if (typeof validarFormulario === 'function') {
                        validarFormulario();
                    }
                } else {
                    calculosContainer.innerHTML = '<p>No hay cálculos disponibles para este jugador.</p>';
                    guardarBtn.disabled = true;
                }
            })
            .catch(error => {
                console.error("Error al cargar datos:", error);
                puestoInput.value = "Error al cargar datos";
                calculosContainer.innerHTML = '<p class="text-center text-danger">Error al cargar cualidades.</p>';
                acordeon.innerHTML = '<p class="text-center text-danger">Error al cargar estadísticas.</p>';
                guardarBtn.disabled = true;
            });
    } else {
        // Mostrar mensaje si no se selecciona un jugador
        calculosContainer.innerHTML = '<p>Seleccione un jugador para ver los cálculos.</p>';
        acordeon.innerHTML = '<p>Seleccione un jugador para cargar las estadísticas.</p>';
        guardarBtn.disabled = true;
    }
});

// Sobrescribir el evento de actualización con cálculos y validaciones dinámicas
document.getElementById("valoracion-form").addEventListener("input", function () {
    if (typeof validarFormulario === 'function') {
        validarFormulario(); // Validar el formulario en cada input
    }
    if (typeof actualizarCabecera === 'function') {
        actualizarCabecera(); // Calcular valores dinámicos
    }
});
