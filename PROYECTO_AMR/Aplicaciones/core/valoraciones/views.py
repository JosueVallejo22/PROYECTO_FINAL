from django.shortcuts import render
from django.views.generic import TemplateView, View
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.valoraciones.models import *
from Aplicaciones.paneladmin.submodulos.models import *
from django.http import JsonResponse
from django.utils.timezone import now

# Vista para el módulo principal de valoraciones
class ModuloValoracionesView(TemplateView):
    template_name = "modulo_valoraciones.html"

class GenerarValoracionView(TemplateView):
    template_name = "valoracion_formulario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener jugadores activos
        jugadores = Jugador.objects.filter(estado=True)

        # Obtener la fecha actual
        fecha_actual = now().date()

        # Procesar cualidades y estadísticas relacionadas
        cualidades = []
        max_estadisticas = 0

        for pc in PuestoCualidad.objects.all():
            estadisticas = list(
                Estadistica.objects.filter(cualidad=pc.cualidad, estado=True)
                .values_list('estadistica', flat=True)
            )
            cualidades.append({
                "cualidad": pc.cualidad.cualidad,
                "estadisticas": estadisticas
            })
            max_estadisticas = max(max_estadisticas, len(estadisticas))

        # Crear una estructura de filas para la tabla
        filas = []
        for i in range(max_estadisticas):
            fila = []
            for cualidad in cualidades:
                if i < len(cualidad['estadisticas']):
                    fila.append(cualidad['estadisticas'][i])
                else:
                    fila.append(None)
            filas.append(fila)

        # Agregar datos al contexto
        context.update({
            'jugadores': jugadores,
            'fecha_actual': fecha_actual,
            'cualidades': cualidades,
            'filas': filas,  # Fila organizada con estadísticas
        })
        return context

class CargarCualidadesView(View):
    def get(self, request, jugador_id):
        try:
            # Obtener el jugador seleccionado
            jugador = Jugador.objects.get(id=jugador_id, estado=True)
            puesto = jugador.puesto  # Obtener el puesto del jugador

            # Verificar si el jugador tiene puesto y posición asociados
            puesto_nombre = puesto.abreviatura if puesto else "Sin puesto asignado"
            posicion_nombre = puesto.posicion.posicion if puesto and puesto.posicion else "Sin posición asignada"

            # Filtrar cualidades asociadas al puesto del jugador
            puesto_cualidades = PuestoCualidad.objects.filter(puesto=puesto, estado=True)

            # Preparar las cualidades y las estadísticas asociadas
            cualidades = []
            for pc in puesto_cualidades:
                estadisticas = Estadistica.objects.filter(cualidad=pc.cualidad, estado=True)
                cualidades.append({
                    "cualidad": pc.cualidad.cualidad,  # Nombre de la cualidad
                    "estadisticas": [
                        {"nombre": est.estadistica} for est in estadisticas
                    ],  # Lista de estadísticas asociadas
                })

            # Preparar respuesta JSON
            data = {
                "puesto": f"{puesto_nombre} - {posicion_nombre}",
                "cualidades": cualidades,
            }
            return JsonResponse(data)
        except Jugador.DoesNotExist:
            return JsonResponse({"error": "Jugador no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
