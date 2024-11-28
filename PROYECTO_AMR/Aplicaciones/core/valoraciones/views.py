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
from django.db.models import Q, Count, Sum
from Aplicaciones.core.views import login_required
from django.utils.decorators import method_decorator
from Aplicaciones.Auditoria.utils import save_audit
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string

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
                    "estadisticas": [{"id": est.id, "nombre": est.estadistica, "descripcion": est.descripcion, "clave": est.estadistica.upper()} for est in estadisticas]
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

                # Guardar auditoría
                save_audit(self.request, valoracion, action='A')  # Acción 'A' para agregar
                
                #Enviar PDF
                pdf_content = self.generar_pdf(valoracion)
                self.enviar_correo(jugador, pdf_content)

                if valoracion.valoracion_total < 70:
                    self.enviar_correo_administradores(jugador, valoracion)

                messages.success(self.request, "Valoración guardada exitosamente.")
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f"Error al guardar la valoración: {e}")
            return redirect(self.success_url)


    def form_invalid(self, form):
        messages.error(self.request, "Formulario inválido. Verifique los datos ingresados.")
        return redirect(self.success_url)
    
    def generar_pdf(self, valoracion):
        """Generar el PDF con xhtml2pdf usando el HTML específico."""
        # Filtrar cualidades asociadas al puesto del jugador
        cualidades_asociadas = PuestoCualidad.objects.filter(puesto=valoracion.jugador.puesto).select_related('cualidad')

        # Crear una lista dinámica de las cualidades con sus valores
        cualidades = []
        for puesto_cualidad in cualidades_asociadas:
            cualidad_nombre = puesto_cualidad.cualidad.cualidad.lower()
            valor_cualidad = getattr(valoracion, f"valoracion_{cualidad_nombre}", None)
            cualidades.append({'nombre': puesto_cualidad.cualidad.cualidad, 'valor': valor_cualidad})

        # Contexto para la plantilla
        context = {
            'valoracion': valoracion,
            'jugador': valoracion.jugador,
            'cualidades': cualidades,
            'estadisticas': valoracion.detalles.all(),
            'fecha': date.today(),
            'current_year': date.today().year,
        }

        # Renderizar el HTML del PDF
        html = render_to_string('reporte_valoraciones_detalle.html', context)
        pdf = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf)

        return pdf.getvalue()

    def enviar_correo(self, jugador, pdf_content):
        """Enviar el correo con el PDF adjunto."""
        email = EmailMessage(
            subject="Reporte de Valoración",
            body=f"Hola {jugador.nombre},\n\nSe te ha evaluado, a continuacion te adjuntamos el reporte de tu valoracion.",
            from_email="svallejos@unemi.edu.ec",
            to=[jugador.correo],
        )
        email.attach(f"valoracion_{jugador.nombre}.pdf", pdf_content, "application/pdf")
        email.send()

    def enviar_correo_administradores(self, jugador, valoracion):
        """Enviar el correo a los administradores si el rendimiento es deficiente."""
        # Obtener correos de los administradores
        administradores = Usuario.objects.filter(rol__rol='ADMINISTRADOR').values_list('correo', flat=True)

        # Generar PDF
        pdf_content = self.generar_pdf(valoracion)

        # Cuerpo del correo
        body = (
            f"El jugador {jugador.nombre} {jugador.apellido} ha obtenido un rendimiento deficiente "
            f"con una valoración total de {valoracion.valoracion_total}.\n\n"
            "Se adjunta el reporte de la evaluación para más detalles."
        )

        # Enviar el correo
        email = EmailMessage(
            subject="Alerta: Rendimiento Deficiente",
            body=body,
            from_email="svallejos@unemi.edu.ec",
            to=list(administradores),
        )
        email.attach(f"reporte_rendimiento_{jugador.nombre}.pdf", pdf_content, "application/pdf")
        email.send()
    
#######################
#DASHBOARDS#

###### PRIMER DASHBOARD ######

@method_decorator(login_required, name='dispatch')
class DashboardsView(TemplateView):
    template_name = 'dashboards.html'

    def get_context_data(self, **kwargs):
        """
        Agrega al contexto los jugadores activos y la distribución por puesto.
        """
        context = super().get_context_data(**kwargs)
        context['jugadores'] = Jugador.objects.filter(estado=True)

        # Consulta: Cantidad de jugadores por puesto
        context['puestos'] = Puesto.objects.filter(estado=True).annotate(total_jugadores=Count('jugador'))

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

class ObtenerDatosDistribucionView(View):
    def get(self, request, *args, **kwargs):
        """
        Devuelve la cantidad de jugadores por puesto en formato JSON,
        considerando solo los jugadores activos.
        """
        # Filtrar puestos activos y contar solo jugadores activos
        puestos = Puesto.objects.filter(estado=True).annotate(
            total_jugadores=Count('jugador', filter=Q(jugador__estado=True))
        )
        datos = {
            "puestos": [{"puesto": p.puesto, "total_jugadores": p.total_jugadores} for p in puestos]
        }
        return JsonResponse(datos)

from django.db.models import Count, Sum, Q

# Vista API para datos de penales atajados
class ObtenerDatosPenalesView(View):
    def get(self, request, jugador_id=None, *args, **kwargs):
        """
        Devuelve en formato JSON la tasa de éxito en penales atajados.
        Si jugador_id es None, calcula para todos los arqueros.
        """
        if jugador_id:
            # Filtrar estadísticas para un arquero específico
            jugador = get_object_or_404(Jugador, id=jugador_id, puesto__puesto__icontains="portero")
            penales_recibidos = ValoracionDetalle.objects.filter(
                valoracion__jugador=jugador, 
                estadistica__estadistica="PENALES RECIBIDOS"
            ).aggregate(total=Sum('valor'))['total'] or 0

            penales_atajados = ValoracionDetalle.objects.filter(
                valoracion__jugador=jugador, 
                estadistica__estadistica="PENALES ATAJADOS"
            ).aggregate(total=Sum('valor'))['total'] or 0

            tasa_exito = (penales_atajados / penales_recibidos * 100) if penales_recibidos > 0 else 0

            datos = {
                "jugadores": [
                    {
                        "nombre": f"{jugador.nombre} {jugador.apellido}",
                        "penales_recibidos": penales_recibidos,
                        "penales_atajados": penales_atajados,
                        "tasa_exito": round(tasa_exito, 2),
                    }
                ]
            }
        else:
            # Calcular estadísticas para todos los porteros
            porteros = Jugador.objects.filter(estado=True, puesto__puesto__icontains="portero")
            jugadores_datos = []

            for portero in porteros:
                penales_recibidos = ValoracionDetalle.objects.filter(
                    valoracion__jugador=portero, 
                    estadistica__estadistica="PENALES RECIBIDOS"
                ).aggregate(total=Sum('valor'))['total'] or 0

                penales_atajados = ValoracionDetalle.objects.filter(
                    valoracion__jugador=portero, 
                    estadistica__estadistica="PENALES ATAJADOS"
                ).aggregate(total=Sum('valor'))['total'] or 0

                tasa_exito = (penales_atajados / penales_recibidos * 100) if penales_recibidos > 0 else 0

                jugadores_datos.append({
                    "nombre": f"{portero.nombre} {portero.apellido}",
                    "penales_recibidos": penales_recibidos,
                    "penales_atajados": penales_atajados,
                    "tasa_exito": round(tasa_exito, 2),
                })

            datos = {"jugadores": jugadores_datos}

        return JsonResponse(datos)
#################################