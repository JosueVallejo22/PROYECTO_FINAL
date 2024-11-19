document.addEventListener("DOMContentLoaded", function () {
    // Funciones de cálculo para cada cualidad
    // Cálculo de Tiro
function calcularPromedioTiro(valores) {
    const { 'GOLES ANOTADOS': goles, 'TIROS TOTALES': tirosTotales, 'TIROS AL ARCO': tirosArco, 'PENALES ANOTADOS': penalesAnotados, 'PENALES EJECUTADOS': penalesTotales } = valores;
    if (!tirosTotales || !tirosArco || !penalesTotales) return 0;

    let promedio = (
        (goles / tirosTotales) +
        (tirosArco / tirosTotales) +
        ((goles / tirosArco) * 1.1) +
        (penalesAnotados / penalesTotales)
    ) / 4 * 100;

    return Math.min(promedio, 100);
}

// Cálculo de Pase
function calcularPromedioPase(valores) {
    const { 'PASES ACERTADOS': pasesAcertados, 'PASES TOTALES': pasesTotales, 'CENTROS ACERTADOS': centrosAcertados, 'CENTROS TOTALES': centrosTotales } = valores;
    if (!pasesTotales || !centrosTotales) return 0;

    let promedio = (
        (pasesAcertados / pasesTotales) +
        (centrosAcertados / centrosTotales)
    ) / 2 * 100;

    return Math.min(promedio, 100);
}

// Cálculo de Velocidad
function calcularPromedioVelocidad(valores) {
    const { 'SPRINT': sprint, 'ACELERACION': aceleracion } = valores;

    let promedio = (
        (sprint / 42) +
        (aceleracion / 35.28)
    ) / 2 * 100;

    return Math.min(promedio, 100);
}

// Cálculo de Regate
function calcularPromedioRegate(valores) {
    const { 'REGATES EXITOSOS': regatesExitosos, 'REGATES TOTALES': regatesTotales, 'DUELOS GANADOS': duelosGanados, 'DUELOS TOTALES': duelosTotales } = valores;
    if (!regatesTotales || !duelosTotales) return 0;

    let promedio = (
        (regatesExitosos / regatesTotales) +
        (duelosGanados / duelosTotales)
    ) / 2 * 100;

    return Math.min(promedio, 100);
}

// Cálculo de Defensa
function calcularPromedioDefensa(valores) {
    const { 'INTERCEPCIONES EXITOSAS': intercepcionesExitosas, 'INTERCEPCIONES INTENTOS': intercepcionesTotales, 'DESPEJES EXITOSOS': despejesExitosos, 'DESPEJES INTENTOS': despejesTotales } = valores;
    if (!intercepcionesTotales || !despejesTotales) return 0;

    let promedio = (
        ((intercepcionesExitosas / intercepcionesTotales) * 1.1) +
        (despejesExitosos / despejesTotales)
    ) / 2 * 100;

    return Math.min(promedio, 100);
}

// Cálculo de Físico
function calcularPromedioFisico(valores) {
    const { 'SALTO EVALUADO': salto, 'DISTANCIA RECORRIDA': distancia, 'SPRINTS REALIZADOS': sprints, 'FUERZA EXPLOSIVA EVALUADA': fuerzaExplosiva, 'FUERZA ISOMETRICA EVALUADA': fuerzaIsometrica, 'FUERZA RESISTENCIA EVALUADA': resistencia } = valores;

    let promedio = (
        (salto / 100) +
        (distancia / 1000) +
        (sprints / 15) +
        (fuerzaExplosiva / 200) +
        (fuerzaIsometrica / 180) +
        (resistencia / 25)
    ) / 6 * 100;

    return Math.min(promedio, 100);
}

// Cálculo de Reflejos
function calcularPromedioReflejos(valores) {
    const { 'PENALES ATAJADOS': penalesAtajados, 'PENALES RECIBIDOS': penalesRecibidos, '1V1 GANADOS': unoVsUnoGanados, '1V1 TOTALES': unoVsUnoTotales, 'ATAJADAS CRITICAS REFLEJOS': atajadasCriticas, 'TIROS BLOQUEADOS REFLEJOS': tirosBloqueados } = valores;
    if (!penalesRecibidos || !unoVsUnoTotales || !tirosBloqueados) return 0;

    let promedio = (
        (penalesAtajados / penalesRecibidos * 1.5) +
        (unoVsUnoGanados / unoVsUnoTotales) +
        (atajadasCriticas / tirosBloqueados)
    ) / 3 * 100 * 1.1;

    return Math.min(promedio, 100);
}

// Cálculo de Manejo
function calcularPromedioManejo(valores) {
    const { 'TIROS BLOQUEADOS MANEJO': tirosBloqueados, 'TIROS AL ARCO': tirosArco, 'DESPEJES EXITOSOS': despejesExitosos, 'DESPEJES TOTALES': despejesTotales, 'ATRAPES SIN REBOTE': atrapadasSinRebote, 'BALONES ATRAPADOS': balonesAtrapados } = valores;
    if (!tirosArco || !despejesTotales || !balonesAtrapados) return 0;

    let promedio = (
        (tirosBloqueados / tirosArco) +
        (despejesExitosos / despejesTotales) +
        (atrapadasSinRebote / balonesAtrapados)
    ) / 3 * 100 * 1.1;

    return Math.min(promedio, 100);
}

// Cálculo de Saque
function calcularPromedioSaque(valores) {
    const { 'SAQUES LARGOS EXITOSOS': saquesLargosExitosos, 'SAQUES LARGOS INTENTOS': saquesLargosTotales, 'SAQUES CORTOS EXITOSOS': saquesCortosExitosos, 'SAQUES CORTOS INTENTOS': saquesCortosTotales } = valores;
    if (!saquesLargosTotales || !saquesCortosTotales) return 0;

    let promedio = (
        (saquesLargosExitosos / saquesLargosTotales) +
        (saquesCortosExitosos / saquesCortosTotales)
    ) / 2 * 100;

    return Math.min(promedio, 100);
}


    // Mapeo de cualidades a funciones de cálculo
    const calculadores = {
        'TIRO': calcularPromedioTiro,
        'PASE': calcularPromedioPase,
        'VELOCIDAD': calcularPromedioVelocidad,
        'REGATE': calcularPromedioRegate,
        'DEFENSA': calcularPromedioDefensa,
        'FISICO': calcularPromedioFisico,
        'REFLEJOS': calcularPromedioReflejos,
        'MANEJO': calcularPromedioManejo,
        'SAQUE': calcularPromedioSaque,
    };

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

    // Actualiza los campos de las cualidades en la cabecera
    function actualizarCabecera() {
        const valores = obtenerValoresEstadisticas();
        Object.keys(calculadores).forEach(cualidad => {
            const calculador = calculadores[cualidad];
            const promedio = calculador(valores);
            const campo = document.getElementById(`calculo_${cualidad}`);
            if (campo) {
                campo.value = isNaN(promedio) ? "N/A" : promedio.toFixed(2);
            }
        });
    }

    // Listener para cambios en los inputs de estadísticas
    document.getElementById("valoracion-form").addEventListener("input", actualizarCabecera);

    // Cargar cualidades y estadísticas al cambiar el jugador
    document.getElementById("jugador").addEventListener("change", function () {
        const jugadorId = this.value;
        const puestoInput = document.getElementById("puesto");
        const calculosContainer = document.getElementById("calculos-container");
        const acordeon = document.getElementById("accordionEstadisticas");
        const guardarBtn = document.getElementById("guardar-btn");

        if (jugadorId) {
            fetch(`/cargar-cualidades/${jugadorId}/`)
                .then(response => response.json())
                .then(data => {
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
                                    <td><input type="number" name="estadistica_${estadistica.nombre}" class="form-control estadistica-input"></td>
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

                        guardarBtn.disabled = false;
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
            puestoInput.value = '';
            calculosContainer.innerHTML = '<p>Seleccione un jugador para ver los cálculos.</p>';
            guardarBtn.disabled = true;
        }
    });
});

