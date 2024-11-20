document.addEventListener("DOMContentLoaded", function () {
    const guardarBtn = document.getElementById("guardar-btn");

    // Función para deshabilitar el botón al cargar
    if (guardarBtn) guardarBtn.disabled = true;

    // Función para calcular el valor máximo permitido para una estadística
    function calcularMaximo(nombre, valores) {
        switch (nombre) {
            case 'TIROS AL ARCO':
                return valores['TIROS TOTALES'] || 0;
            case 'GOLES ANOTADOS':
                return valores['TIROS AL ARCO'] || 0;
            case 'PENALES ANOTADOS':
                return valores['PENALES EJECUTADOS'] || 0;
            case 'PASES ACERTADOS':
                return valores['PASES TOTALES'] || 0;
            case 'CENTROS ACERTADOS':
                return valores['CENTROS TOTALES'] || 0;
            case 'REGATES EXITOSOS':
                return valores['REGATES TOTALES'] || 0;
            case 'DUELOS EXITOSOS':
                return valores['DUELOS TOTALES'] || 0;
            case 'INTERCEPCIONES EXITOSAS':
                return valores['INTERCEPCIONES INTENTOS'] || 0;
            case 'DUELOS DEFENSIVOS GANADOS':
                return valores['DUELOS DEFENSIVOS TOTALES'] || 0;
            case 'PENALES ATAJADOS':
                return valores['PENALES RECIBIDOS'] || 0;
            case '1V1 GANADOS':
                return valores['1V1 TOTALES'] || 0;
            case 'ATAJADAS CRITICAS REFLEJOS':
                return valores['TIROS BLOQUEADOS REFLEJOS'] || 0;
            case 'TIROS BLOQUEADOS MANEJO':
                return valores['TIROS TOTALES RECIBIDOS'] || 0;
            case 'DESPEJES EXITOSOS':
                return valores['DESPEJES TOTALES'] || 0;
            case 'ATRAPES SIN REBOTE':
                return valores['BALONES ATRAPADOS'] || 0;
            case 'SAQUES LARGOS EXITOSOS':
                return valores['SAQUES LARGOS INTENTOS'] || 0;
            case 'SAQUES CORTOS EXITOSOS':
                return valores['SAQUES CORTOS INTENTOS'] || 0;
            default:
                return null;
        }
    }

    // Función para validar los campos dinámicos
    function validarCampo(input) {
        const nombre = input.name.replace("estadistica_", "");
        const valor = parseFloat(input.value) || 0;

        const valores = obtenerValoresEstadisticas();
        const maximo = calcularMaximo(nombre, valores);

        let errorDiv = input.nextElementSibling;
        if (!errorDiv || !errorDiv.classList.contains("invalid-feedback")) {
            errorDiv = document.createElement("div");
            errorDiv.className = "invalid-feedback";
            input.insertAdjacentElement("afterend", errorDiv);
        }

        // Validar el valor ingresado
        if (valor < 0) {
            input.classList.add("is-invalid");
            errorDiv.textContent = "El valor no puede ser negativo.";
        } else if (maximo !== null && valor > maximo) {
            input.classList.add("is-invalid");
            errorDiv.textContent = `El valor no puede ser mayor a ${maximo}.`;
        } else {
            input.classList.remove("is-invalid");
            errorDiv.textContent = "";
        }
    }

    // Validar todo el formulario y actualizar el estado del botón "Guardar"
    function validarFormulario() {
        const hayErrores = document.querySelectorAll(".is-invalid").length > 0;
        const jugadorSeleccionado = document.getElementById("jugador").value !== "";

        // Comprobar si todos los campos de estadística están llenos (permitiendo 0 como válido)
        const camposDetalle = document.querySelectorAll('.estadistica-input');
        const todosCamposLlenos = Array.from(camposDetalle).every(input => input.value.trim() !== "");

        if (guardarBtn) {
            guardarBtn.disabled = hayErrores || !jugadorSeleccionado || !todosCamposLlenos;
        }
    }

    // Obtener valores de los inputs dinámicos
    function obtenerValoresEstadisticas() {
        const valores = {};
        document.querySelectorAll('.estadistica-input').forEach(input => {
            const estadisticaNombre = input.name.replace("estadistica_", "");
            const valor = parseFloat(input.value) || 0;
            valores[estadisticaNombre] = valor;
        });
        return valores;
    }

    // Listeners para validar inputs dinámicos
    document.addEventListener("input", function (e) {
        if (e.target && e.target.classList.contains("estadistica-input")) {
            validarCampo(e.target);
            validarFormulario();
        }
    });

    // Listener para actualizar validaciones cuando cambie el jugador
    document.getElementById("jugador").addEventListener("change", function () {
        validarFormulario();
    });

    // Validar inicialmente al cargar
    validarFormulario();
});
