document.addEventListener("DOMContentLoaded", function () {
    // Configurar la fecha y hora actual
    const fechaInput = document.getElementById("fecha");
    const horaInput = document.getElementById("hora");

    const ahora = new Date();
    const fechaActual = ahora.toLocaleDateString("es-ES", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
    });

    const horaActual = ahora.toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });

    fechaInput.value = fechaActual;
    horaInput.value = horaActual;

    // Función para calcular el promedio de Pase
    function calcularPromedioPase(valores) {
        const { 'PASES ACERTADOS': pases_acertados, 'PASES TOTALES': pases_totales, 'CENTROS ACERTADOS': centros_acertados, 'CENTROS TOTALES': centros_totales } = valores;

        if (pases_totales === 0 || centros_totales === 0) return 0;

        let promedio = ((pases_acertados / pases_totales) + (centros_acertados / centros_totales)) / 2 * 100;
        return Math.min(promedio, 100);
    }

    // Función para calcular el promedio de Tiro
    function calcularPromedioTiro(valores) {
        const { 'GOLES ANOTADOS': goles_anotados, 'TIROS TOTALES': tiros_totales, 'TIROS AL ARCO': tiros_al_arco, 'PENALES ANOTADOS': penales_anotados, 'PENALES EJECUTADOS': penales_ejecutados } = valores;

        if (tiros_totales === 0 || tiros_al_arco === 0 || penales_ejecutados === 0) return 0;

        let promedio = (( 
            (goles_anotados / tiros_totales) +
            (tiros_al_arco / tiros_totales) +
            ((goles_anotados / tiros_al_arco) * 1.1) +
            (penales_anotados / penales_ejecutados)
        ) / 4 ) * 100;

        return Math.min(promedio, 100);
    }

    // Función para actualizar los campos de la cabecera con los cálculos
    function actualizarCabecera(cualidades) {
        cualidades.forEach(cualidad => {
            const input = document.getElementById(`calculo_${cualidad.cualidad}`);
            if (input) {
                input.value = cualidad.valor.toFixed(2); // Mostrar valor con dos decimales
            }
        });
    }

    // Evento para manejar el ingreso de las estadísticas
    document.getElementById("valoracion-form").addEventListener("input", function () {
        let valores = {};

        // Obtener las estadísticas ingresadas
        document.querySelectorAll('.estadistica-input').forEach(input => {
            valores[input.name] = parseFloat(input.value) || 0;
        });

        // Realizar los cálculos para cada cualidad
        const cualidades = [
            { cualidad: "Pase", valor: calcularPromedioPase(valores) },
            { cualidad: "Tiro", valor: calcularPromedioTiro(valores) }
            // Agregar más cualidades según sea necesario
        ];

        // Actualizar la cabecera con los valores calculados
        actualizarCabecera(cualidades);
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

                    // Mostrar cualidades en la cabecera
                    if (data.cualidades && data.cualidades.length > 0) {
                        data.cualidades.forEach((cualidad, index) => {
                            const col = document.createElement("div");
                            col.className = "col-md-2 mb-3";
                            col.innerHTML = `
                                <label class="form-label">${cualidad.cualidad}</label>
                                <input type="text" class="form-control" placeholder="Calculado automáticamente" readonly id="calculo_${cualidad.cualidad}">
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
});
