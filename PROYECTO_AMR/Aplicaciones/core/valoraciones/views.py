from django.shortcuts import render
from django.views.generic import *
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.valoraciones.models import *
from Aplicaciones.paneladmin.submodulos.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from Aplicaciones.core.valoraciones.forms import *
# Create your views here.

class SeleccionJugadorView(FormView):
    """
    Vista para seleccionar un jugador.
    """
    template_name = "form_valoraciones.html"
    form_class = SeleccionJugadorForm

    def form_valid(self, form):
        jugador_id = form.cleaned_data["jugador"].id
        return redirect("valoracion_jugador", jugador_id=jugador_id)


def valorar_jugador(request, jugador_id):
    """
    Vista para mostrar las estadísticas y cualidades relacionadas con el jugador seleccionado.
    """
    jugador = get_object_or_404(Jugador, id=jugador_id)

    # Obtener las cualidades asociadas al puesto del jugador
    puesto = jugador.puesto
    cualidades = PuestoCualidad.objects.filter(puesto=puesto).select_related("cualidad")

    # Obtener las estadísticas asociadas a esas cualidades
    estadisticas = Estadistica.objects.filter(cualidad__in=cualidades.values_list("cualidad", flat=True))

    if request.method == "POST":
        form = EstadisticasValoracionForm(request.POST, estadisticas=estadisticas)
        if form.is_valid():
            # Crear la valoración
            valoracion = Valoracion.objects.create(jugador=jugador, descripcion="Valoración generada")

            # Guardar los detalles de la valoración
            for field_name, valor in form.cleaned_data.items():
                if field_name.startswith("estadistica_") and valor is not None:
                    estadistica_id = int(field_name.split("_")[1])
                    estadistica = get_object_or_404(Estadistica, id=estadistica_id)
                    ValoracionDetalle.objects.create(
                        valoracion=valoracion,
                        estadistica=estadistica,
                        valor=valor,
                    )

            return redirect("valoracion_exitosa")  # Redirige a una página de éxito
    else:
        form = EstadisticasValoracionForm(estadisticas=estadisticas)

    context = {
        "jugador": jugador,
        "cualidades": cualidades,
        "form": form,
    }
    return render(request, "form_valoraciones_detalle.html", context)