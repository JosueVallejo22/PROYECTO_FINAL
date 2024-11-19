from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.db import transaction
from django.http import JsonResponse
from django.utils.timezone import now
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.valoraciones.models import *
from Aplicaciones.paneladmin.submodulos.models import *
from Aplicaciones.core.valoraciones.forms import ValoracionForm, ValoracionDetalleForm

# Vista para el módulo principal de valoraciones
class ModuloValoracionesView(TemplateView):
    template_name = "modulo_valoraciones.html"

# Vista para el formulario de generar una nueva valoración
class GenerarValoracionView(TemplateView):
    template_name = "valoracion_formulario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener jugadores activos
        jugadores = Jugador.objects.filter(estado=True)

        # Obtener la fecha y hora actual
        fecha_actual = now().date()
        hora_actual = now().time()

        # Pasar los jugadores y la fecha al contexto
        context.update({
            'jugadores': jugadores,
            'fecha_actual': fecha_actual,
            'hora_actual': hora_actual,
        })
        
        return context

# Cargar cualidades del jugador seleccionado
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

# Crear valoración, incluyendo la cabecera y los detalles
class CrearValoracionView(FormView):
    template_name = 'valoracion_formulario.html'
    form_class = ValoracionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener jugadores activos y la fecha actual
        jugadores = Jugador.objects.filter(estado=True)
        fecha_actual = now().date()
        hora_actual = now().time()
        
        context.update({
            'jugadores': jugadores,
            'fecha_actual': fecha_actual,
            'hora_actual': hora_actual,
        })

        # Inicialmente no hay jugador seleccionado
        context['jugador'] = None
        
        return context

    def form_valid(self, form):
        # Usamos una transacción atómica para guardar ambos modelos de forma segura
        with transaction.atomic():
            # Guardar la cabecera de la valoración
            valoracion = form.save()

            # Obtener el formulario de detalles con las estadísticas
            detalle_form = ValoracionDetalleForm(self.request.POST)
            
            if detalle_form.is_valid():
                # Guardar cada detalle de valoración
                for field, value in detalle_form.cleaned_data.items():
                    if value:
                        try:
                            # Extraemos el ID de la estadística del nombre del campo (formato 'estadistica_{id}')
                            estadistica_id = field.split('_')[1]
                            estadistica = get_object_or_404(Estadistica, pk=estadistica_id)

                            # Crear un registro en ValoracionDetalle
                            ValoracionDetalle.objects.create(
                                valoracion=valoracion,
                                estadistica=estadistica,
                                valor=value
                            )
                        except IndexError:
                            return JsonResponse({"error": "Formato de campo inválido"}, status=400)

            # Redirigir al usuario después de guardar correctamente
            return redirect('valoraciones:success')

    def form_invalid(self, form):
        return JsonResponse({"error": "Formulario inválido"}, status=400)
