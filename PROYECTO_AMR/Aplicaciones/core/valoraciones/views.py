from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *
from django.views.generic.edit import FormView
from django.db import transaction
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse_lazy
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.valoraciones.models import *
from Aplicaciones.paneladmin.submodulos.models import *
from Aplicaciones.core.valoraciones.forms import ValoracionForm, ValoracionDetalleForm
from django.db.models import Q
from Aplicaciones.core.views import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ModuloValoracionesView(ListView):
    model = Valoracion
    template_name = 'modulo_valoraciones.html'
    context_object_name = 'valoraciones'
    paginate_by = 5

    def get_queryset(self):
        # Obtener el queryset inicial
        queryset = super().get_queryset().select_related('jugador', 'jugador__puesto').order_by('-id')

        # Obtener parámetros de búsqueda y filtro
        search_query = self.request.GET.get('search', '')
        puesto_filter = self.request.GET.get('puesto', '')

        # Aplicar filtro por búsqueda (jugador o fecha)
        if search_query:
            queryset = queryset.filter(
                Q(jugador__nombre__icontains=search_query) |
                Q(jugador__apellido__icontains=search_query)
            )

        # Aplicar filtro por posición (puesto del jugador)
        if puesto_filter:
            queryset = queryset.filter(jugador__puesto__id=puesto_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Agregar lista de puestos para los filtros
        context['puestos'] = Puesto.objects.all().order_by('puesto')

        # Obtener los detalles de la valoración si se envía el parámetro "detalle"
        detalle_id = self.request.GET.get('detalle')
        if detalle_id:
            try:
                # Obtener la valoración
                detalle_valoracion = Valoracion.objects.select_related('jugador__puesto').get(pk=detalle_id)
                context['detalle_valoracion'] = detalle_valoracion

                # Obtener las cualidades asociadas al puesto del jugador
                cualidades_puesto = PuestoCualidad.objects.filter(
                    puesto=detalle_valoracion.jugador.puesto,
                    estado=True  # Filtrar solo las activas
                ).select_related('cualidad')

                # Construir un diccionario de cualidades y valores desde la cabecera
                cualidades_evaluadas = []
                for puesto_cualidad in cualidades_puesto:
                    cualidad_nombre = puesto_cualidad.cualidad.cualidad.lower()
                    valor_campo = f"valoracion_{cualidad_nombre}"
                    valor = getattr(detalle_valoracion, valor_campo, None)  # Accede dinámicamente al campo
                    if valor is not None:
                        cualidades_evaluadas.append({
                            'nombre': puesto_cualidad.cualidad.cualidad,
                            'valor': valor,
                        })

                context['cualidades_evaluadas'] = cualidades_evaluadas

            except Valoracion.DoesNotExist:
                context['detalle_valoracion'] = None
                context['cualidades_evaluadas'] = []
        return context


# Vista para el formulario de generar una nueva valoración
@method_decorator(login_required, name='dispatch')
class CrearValoracionView(TemplateView):
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
@method_decorator(login_required, name='dispatch')
class CargarCualidadesView(View):
    def get(self, request, jugador_id):
        try:
            # Obtener el jugador seleccionado
            jugador = get_object_or_404(Jugador, id=jugador_id, estado=True)
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
                    "peso": float(pc.peso),  # Convertir peso a float para el frontend
                    "estadisticas": [{"id": est.id, "nombre": est.estadistica, "clave": est.estadistica.upper()} for est in estadisticas]
                })

            # Preparar respuesta JSON
            data = {
                "puesto": f"{puesto_nombre} - {posicion_nombre}",
                "cualidades": cualidades,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)


@method_decorator(login_required, name='dispatch')
class GuardarValoracionView(FormView):
    template_name = 'valoracion_formulario.html'
    form_class = ValoracionForm
    success_url = reverse_lazy('valoraciones:modulo_valoraciones')  # Redirige al listado tras guardar

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Obtener jugador y descripción
                jugador_id = self.request.POST.get('jugador')
                jugador = get_object_or_404(Jugador, id=jugador_id)
                descripcion = self.request.POST.get('descripcion', '')

                # Obtener el usuario desde la sesión
                user_id = self.request.session.get('user_id')  # Recupera el ID del usuario desde la sesión
                usuario = get_object_or_404(Usuario, id=user_id)  # Busca el usuario relacionado

                # Crear cabecera de valoración
                valoracion = Valoracion.objects.create(
                    jugador=jugador,
                    descripcion=descripcion,
                    usuario_registro=usuario.nombre_usuario  # Guarda el nombre del usuario
                )

                # Calcular y asignar valores a las cualidades
                cualidades = ['tiro', 'pase', 'velocidad', 'regate', 'defensa', 'fisico', 'reflejos', 'manejo', 'saque']
                suma_ponderada = 0
                total_pesos = 0

                for cualidad in cualidades:
                    promedio_cualidad = float(self.request.POST.get(f'calculo_{cualidad.upper()}', 0))
                    peso_obj = PuestoCualidad.objects.filter(puesto=jugador.puesto, cualidad__cualidad=cualidad).first()
                    peso_valor = float(peso_obj.peso) if peso_obj else 0

                    if promedio_cualidad > 0 and peso_valor > 0:
                        suma_ponderada += promedio_cualidad * peso_valor
                        total_pesos += peso_valor

                    # Asignar cada valor al campo correspondiente
                    setattr(valoracion, f'valoracion_{cualidad}', promedio_cualidad)

                # Obtener las cualidades asociadas al puesto del jugador
                puesto_cualidades = PuestoCualidad.objects.filter(puesto=jugador.puesto, estado=True)
                numero_cualidades = puesto_cualidades.count()  # Número real de cualidades asociadas

                # Calcular la valoración total dividiendo por el número real de cualidades asociadas al jugador
                valoracion.valoracion_total = (suma_ponderada / numero_cualidades) if numero_cualidades > 0 else 0
                valoracion.valoracion_total = min(valoracion.valoracion_total, 100)  # Limitar el máximo a 100
                # Guardar la cabecera
                valoracion.save()

                # Guardar detalles de estadísticas
                for key, value in self.request.POST.items():
                    if key.startswith('estadistica_'):
                        estadistica_nombre = key.split('_')[1]
                        estadistica = get_object_or_404(Estadistica, estadistica=estadistica_nombre)
                        ValoracionDetalle.objects.create(
                            valoracion=valoracion,
                            estadistica=estadistica,
                            valor=float(value),
                            usuario_registro=usuario.nombre_usuario  # Usa el mismo usuario
                        )

                messages.success(self.request, "Valoración guardada exitosamente.")
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f"Error al guardar la valoración: {e}")
            return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Formulario inválido. Verifique los datos ingresados.")
        return redirect(self.success_url)
    
#######################
#DASHBOARDS#

###### PRIMER DASHBOARD ######

class DashboardsView(TemplateView):
    template_name = 'dashboards.html'

    def get_context_data(self, **kwargs):
        """
        Agrega al contexto la lista de jugadores activos para ser utilizada en el frontend.
        """
        context = super().get_context_data(**kwargs)
        context['jugadores'] = Jugador.objects.filter(estado=True)
        return context


# API PARA OBTENER LOS DATOS DE VALORACIÓN DE UN JUGADOR
class ObtenerDatosValoracionView(View):
    def get(self, request, jugador_id, *args, **kwargs):
        """
        Devuelve en formato JSON la evolución de valoraciones totales
        de un jugador específico ordenadas por fecha.
        """
        jugador = get_object_or_404(Jugador, id=jugador_id)
        valoraciones = Valoracion.objects.filter(jugador=jugador).order_by('fecha_registro')

        datos = {
            "jugador": f"{jugador.nombre} {jugador.apellido}",
            "fechas": [v.fecha_registro.strftime('%Y-%m-%d') for v in valoraciones],
            "valoraciones_totales": [v.valoracion_total for v in valoraciones],
        }
        return JsonResponse(datos)
