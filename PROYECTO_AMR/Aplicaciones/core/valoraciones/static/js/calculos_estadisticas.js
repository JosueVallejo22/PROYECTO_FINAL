document.addEventListener("DOMContentLoaded", function () {
    // Función para calcular el promedio de tiro
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

    // Función para calcular el promedio de pase
    function calcularPromedioPase(valores) {
        const { 'PASES ACERTADOS': pases_acertados, 'PASES TOTALES': pases_totales, 'CENTROS ACERTADOS': centros_acertados, 'CENTROS TOTALES': centros_totales } = valores;

        if (pases_totales === 0 || centros_totales === 0) return 0;

        let promedio = (
            (pases_acertados / pases_totales) +
            (centros_acertados / centros_totales)
        ) / 2 * 100;

        return Math.min(promedio, 100);
    }

    // Función para calcular el promedio de velocidad
    function calcularPromedioVelocidad(valores) {
        const { 'SPRINT': sprint_kmh, 'ACELERACION': aceleracion_kmh } = valores;

        let promedio = (
            (sprint_kmh / 42) +
            (aceleracion_kmh / 35.28)
        ) / 2 * 100;

        return Math.min(promedio, 100);
    }

    // Función para calcular el promedio de regate
    function calcularPromedioRegate(valores) {
        const { 'REGATES EXITOSOS': regates_exitosos, 'REGATES TOTALES': regates_intentos, 'DUELOS GANADOS': duelos_ganados, 'DUELOS TOTALES': duelos_intentos } = valores;

        if (regates_intentos === 0 || duelos_intentos === 0) return 0;

        let promedio = (
            (regates_exitosos / regates_intentos) +
            (duelos_ganados / duelos_intentos)
        ) / 2 * 100;

        return Math.min(promedio, 100);
    }

    // Función para calcular el promedio de defensa
    function calcularPromedioDefensa(valores) {
        const { 'INTERCEPCIONES EXITOSAS': intercepciones_exitosas, 'INTERCEPCIONES INTENTOS': intercepciones_intentos, 'DESPEJES EXITOSOS': despejes_exitosos, 'DESPEJES INTENTOS': despejes_intentos } = valores;

        if (intercepciones_intentos === 0 || despejes_intentos === 0) return 0;

        let promedio = (
            ((intercepciones_exitosas / intercepciones_intentos) * 1.1) +
            (despejes_exitosos / despejes_intentos)
        ) / 2 * 100;

        return Math.min(promedio, 100);
    }

    // Función para calcular el promedio físico
    function calcularPromedioFisico(valores) {
        const { 'SALTO EVALUADO': salto_evaluado, 'DISTANCIA RECORRIDA': distancia_recorrida, 'SPRINTS REALIZADOS': sprints_realizados, 'FUERZA EXPLOSIVA EVALUADA': fuerza_explosiva_evaluada, 'FUERZA ISOMETRICA EVALUADA': fuerza_isometrica_evaluada, 'FUERZA RESISTENCIA EVALUADA': resistencia_evaluada } = valores;

        let promedio = (
            (salto_evaluado / 100) +
            (distancia_recorrida / 1000) +
            (sprints_realizados / 15) +
            (fuerza_explosiva_evaluada / 200) +
            (fuerza_isometrica_evaluada / 180) +
            (resistencia_evaluada / 25)
        ) / 6 * 100;

        return Math.min(promedio, 100);
    }

    // Función para actualizar los campos de la cabecera con los cálculos
    function actualizarCabecera(cualidades) {
        cualidades.forEach(cualidad => {
            const input = document.getElementById(`calculo_${cualidad.cualidad}`);
            if (input) {
                input.value = cualidad.valor.toFixed(2);
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
            { cualidad: "Tiro", valor: calcularPromedioTiro(valores) },
            { cualidad: "Velocidad", valor: calcularPromedioVelocidad(valores) },
            { cualidad: "Regate", valor: calcularPromedioRegate(valores) },
            { cualidad: "Defensa", valor: calcularPromedioDefensa(valores) },
            { cualidad: "Fisico", valor: calcularPromedioFisico(valores) },
        ];

        // Actualizar la cabecera con los valores calculados
        actualizarCabecera(cualidades);
    });
});
