$(document).ready(function () {
    const cualidadesContainer = $("#cualidades-container");
    const estadisticasContainer = $("#estadisticas-container");
    const fechaActual = new Date().toISOString().slice(0, 10);

    // Configurar fechas
    $("#fecha_creacion").val(fechaActual);
    $("#fecha_actualizacion").val(fechaActual);

    // Manejar cambio de jugador
    $("#jugador").change(function () {
        const jugadorId = $(this).val();
        const puestoId = $("#jugador option:selected").data("puesto");

        cualidadesContainer.empty();
        estadisticasContainer.empty();

        if (jugadorId && puestoId) {
            // Filtrar cualidades por puesto
            const cualidadesFiltradas = cualidades.filter(c => c.puesto_id === puestoId);

            cualidadesFiltradas.forEach(cualidad => {
                cualidadesContainer.append(`
                    <div class="col-md-3">
                        <label class="form-label">Promedio ${cualidad.cualidad.cualidad}</label>
                        <input type="text" class="form-control" readonly id="promedio_${cualidad.cualidad.cualidad.toLowerCase()}" data-peso="${cualidad.peso}">
                    </div>
                `);
            });

            // Filtrar estadísticas por cualidades
            const estadisticasFiltradas = estadisticas.filter(e => cualidadesFiltradas.some(c => c.cualidad.id === e.cualidad.id));

            estadisticasFiltradas.forEach((estadistica, index) => {
                estadisticasContainer.append(`
                    <tr>
                        <td>${index + 1}</td>
                        <td>${estadistica.cualidad.cualidad}</td>
                        <td>${estadistica.estadistica}</td>
                        <td><input type="number" class="form-control" name="estadistica_${estadistica.id}"></td>
                    </tr>
                `);
            });
        }
    });

    // Guardar los datos
    $("#guardar").click(function () {
        const data = {
            jugador: $("#jugador").val(),
            fecha_creacion: $("#fecha_creacion").val(),
            fecha_actualizacion: $("#fecha_actualizacion").val(),
            cualidades: [],
            estadisticas: [],
        };

        // Recopilar cualidades
        cualidadesContainer.find("input").each(function () {
            data.cualidades.push({
                nombre: $(this).attr("id").replace("promedio_", ""),
                valor: $(this).val(),
            });
        });

        // Recopilar estadísticas
        estadisticasContainer.find("input").each(function () {
            data.estadisticas.push({
                id: $(this).attr("name").split("_")[1],
                valor: $(this).val(),
            });
        });

        console.log("Datos a guardar:", data);
        // Aquí puedes enviar los datos al backend con AJAX
    });
});
