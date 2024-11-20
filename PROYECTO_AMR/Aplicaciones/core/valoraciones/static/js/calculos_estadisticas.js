document.addEventListener("DOMContentLoaded", function () {
    // Funciones de cálculo para cada cualidad
    function calcularPromedioTiro(valores) {
        const { 'GOLES ANOTADOS': goles, 'TIROS TOTALES': tirosTotales, 'TIROS AL ARCO': tirosArco, 'PENALES ANOTADOS': penalesAnotados, 'PENALES EJECUTADOS': penalesTotales } = valores;
        if (!tirosTotales || !tirosArco || !penalesTotales) return 0;

        let promedio = (
            (goles / tirosTotales) +
            (tirosArco / tirosTotales) +
            ((goles / tirosArco) * 1.1) +
            (penalesAnotados / penalesTotales)
        ) / 4 * 100;

        return Math.round(Math.min(promedio, 100));
    }

    function calcularPromedioPase(valores) {
        const { 'PASES ACERTADOS': pasesAcertados, 'PASES TOTALES': pasesTotales, 'CENTROS ACERTADOS': centrosAcertados, 'CENTROS TOTALES': centrosTotales } = valores;
        if (!pasesTotales || !centrosTotales) return 0;

        let promedio = (
            (pasesAcertados / pasesTotales) +
            (centrosAcertados / centrosTotales)
        ) / 2 * 100;

        return Math.round(Math.min(promedio, 100));
    }

    function calcularPromedioVelocidad(valores) {
        const { 'SPRINT': sprint, 'ACELERACION': aceleracion } = valores;

        let promedio = (
            (sprint / 42) +
            (aceleracion / 35.28)
        ) / 2 * 100;

        return Math.round(Math.min(promedio, 100));
    }

    function calcularPromedioRegate(valores) {
        const { 'REGATES EXITOSOS': regatesExitosos, 'REGATES TOTALES': regatesTotales, 'DUELOS EXITOSOS': duelosExitosos, 'DUELOS TOTALES': duelosTotales } = valores;
        if (!regatesTotales || !duelosTotales) return 0;

        let promedio = (
            (regatesExitosos / regatesTotales) +
            (duelosExitosos / duelosTotales)
        ) / 2 * 100;

        return Math.round(Math.min(promedio, 100));
    }

    function calcularPromedioDefensa(valores) {
        const { 'INTERCEPCIONES EXITOSAS': intercepcionesExitosas, 'INTERCEPCIONES INTENTOS': intercepcionesTotales, 'DUELOS DEFENSIVOS GANADOS': duelosGanados, 'DUELOS DEFENSIVOS TOTALES': duelosTotales } = valores;
        if (!intercepcionesTotales || !duelosTotales) return 0;

        let promedio = (
            (intercepcionesExitosas / intercepcionesTotales) +
            (duelosGanados / duelosTotales)
        ) / 2 * 100;

        return Math.round(Math.min(promedio, 100));
    }

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

        return Math.round(Math.min(promedio, 100));
    }

    function calcularPromedioReflejos(valores) {
        const { 'PENALES ATAJADOS': penalesAtajados, 'PENALES RECIBIDOS': penalesRecibidos, '1V1 GANADOS': unoVsUnoGanados, '1V1 TOTALES': unoVsUnoTotales, 'ATAJADAS CRITICAS REFLEJOS': atajadasCriticas, 'TIROS BLOQUEADOS REFLEJOS': tirosBloqueados } = valores;
        if (!penalesRecibidos || !unoVsUnoTotales || !tirosBloqueados) return 0;

        let promedio = (
            (penalesAtajados / penalesRecibidos * 1.5) +
            (unoVsUnoGanados / unoVsUnoTotales) +
            (atajadasCriticas / tirosBloqueados)
        ) / 3 * 100 * 1.1;

        return Math.round(Math.min(promedio, 100));
    }

    function calcularPromedioManejo(valores) {
        const { 'TIROS BLOQUEADOS MANEJO': tirosBloqueados, 'TIROS TOTALES RECIBIDOS': tirosRecibidos, 'DESPEJES EXITOSOS': despejesExitosos, 'DESPEJES TOTALES': despejesTotales, 'ATRAPES SIN REBOTE': atrapadasSinRebote, 'BALONES ATRAPADOS': balonesAtrapados } = valores;
        if (!tirosRecibidos || !despejesTotales || !balonesAtrapados) return 0;

        let promedio = (
            (tirosBloqueados / tirosRecibidos) +
            (despejesExitosos / despejesTotales) +
            (atrapadasSinRebote / balonesAtrapados)
        ) / 3 * 100;

        return Math.round(Math.min(promedio, 100));
    }

    function calcularPromedioSaque(valores) {
        const { 'SAQUES LARGOS EXITOSOS': saquesLargosExitosos, 'SAQUES LARGOS INTENTOS': saquesLargosTotales, 'SAQUES CORTOS EXITOSOS': saquesCortosExitosos, 'SAQUES CORTOS INTENTOS': saquesCortosTotales } = valores;
        if (!saquesLargosTotales || !saquesCortosTotales) return 0;

        let promedio = (
            (saquesLargosExitosos / saquesLargosTotales) +
            (saquesCortosExitosos / saquesCortosTotales)
        ) / 2 * 100;

        return Math.round(Math.min(promedio, 100));
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

    let pesos = {}; // Aquí almacenaremos los pesos de las cualidades

    // Función para cargar los pesos desde el servidor
    async function cargarPesos(jugadorId) {
        const response = await fetch(`/cargar-cualidades/${jugadorId}/`);
        const data = await response.json();

        pesos = data.cualidades.reduce((acc, cualidad) => {
            acc[cualidad.cualidad] = cualidad.peso; // Mapear los pesos por cualidad
            return acc;
        }, {});
    }

    // Función para actualizar cálculos dinámicos en la cabecera
    function actualizarCabecera() {
        const hayErrores = document.querySelectorAll(".is-invalid").length > 0;
        if (hayErrores) {
            console.log("Errores presentes. No se calculan valores.");
            return; // Ignorar cálculos si hay errores
        }

        const valores = obtenerValoresEstadisticas();
        Object.keys(calculadores).forEach(cualidad => {
            const calculador = calculadores[cualidad];
            const promedio = calculador(valores);

            const campo = document.getElementById(`calculo_${cualidad}`);
            if (campo) {
                campo.value = isNaN(promedio) ? "N/A" : promedio;
            }
        });

        actualizarValoracionFinal(); // Calcular la valoración final después de actualizar las cualidades
    }

    // Función para calcular y mostrar la valoración final
    function actualizarValoracionFinal() {
        let sumaPonderada = 0;
        let sumaPesos = 0;
    
        // Recorrer cada cualidad y calcular su contribución
        Object.keys(pesos).forEach(cualidad => {
            const promedio = parseFloat(document.getElementById(`calculo_${cualidad}`)?.value || 0); // Obtener promedio de la cualidad
            const peso = pesos[cualidad] || 0; // Obtener peso correspondiente desde los datos cargados
    
            sumaPonderada += promedio * peso; // Sumar el promedio ponderado por el peso
            sumaPesos += peso; // Sumar el peso
        });
    
        // Dividir la suma ponderada por el número total de cualidades (6 en este caso)
        const totalCualidades = Object.keys(pesos).length;
        const valoracionFinal = totalCualidades > 0 ? Math.min((sumaPonderada / totalCualidades), 100) : 0;
    
        // Mostrar el resultado
        const campoValoracionFinal = document.getElementById("valoracion_final");
        if (campoValoracionFinal) {
            campoValoracionFinal.value = valoracionFinal.toFixed(2);
        }
    }
    

    // Listeners para cálculos dinámicos
    document.getElementById("valoracion-form").addEventListener("input", actualizarCabecera);

    // Escuchar cambios en inputs dinámicos
    document.getElementById("jugador").addEventListener("change", function () {
        const jugadorId = this.value;
        if (jugadorId) {
            cargarPesos(jugadorId).then(() => {
                // Reasignar listeners a nuevos inputs generados dinámicamente
                setTimeout(() => {
                    document.querySelectorAll(".estadistica-input").forEach(input => {
                        input.addEventListener("input", actualizarCabecera);
                    });
                }, 500); // Esperar la carga de elementos dinámicos
            });
        }
    });
});