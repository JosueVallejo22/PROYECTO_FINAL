from django.shortcuts import get_object_or_404, render
from Aplicaciones.Login.models import *
from Aplicaciones.core.models import *
from Aplicaciones.core.valoraciones.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from xhtml2pdf.pisa import CreatePDF
import datetime
from django.views import *
from django.db.models import Count  # Importar Count para el conteo
from reportlab.pdfgen import canvas
from io import BytesIO


# Create your views here.

##############################################################################################################
# VISTA PARA GENERAR UN REPORTE DEL LISTADO DE USUARIOS EN PDF

class GenerarReporteUsuariosPDF(View):
    def get(self, request, *args, **kwargs):
        # Obtener todos los usuarios y calcular su edad
        usuarios = Usuario.objects.all().order_by('id')  # Ordenamos por ID
        for usuario in usuarios:
            usuario.edad = (datetime.date.today().year - usuario.fecha_nacimiento.year)

        # Calcular el total de usuarios
        total_usuarios = usuarios.count()

        # Calcular el conteo de usuarios por rol
        conteo_por_rol = Usuario.objects.values('rol__rol').annotate(total=Count('id'))

        # Datos para pasar al contexto
        context = {
            'usuarios': usuarios,
            'fecha': datetime.date.today(),
            'total_usuarios': total_usuarios,
            'conteo_por_rol': conteo_por_rol,  # Pasamos los datos por rol
        }

        # Renderizar la plantilla HTML
        html = render_to_string('reporte_usuarios.html', context)

        # Crear la respuesta HTTP con tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'

        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response
    
######################################################################################################################
# VISTA PARA GENERAR REPORTE DE JUGADORES DE FUTBOL
# VISTA PARA GENERAR UN REPORTE DEL LISTADO DE JUGADORES EN PDF

class GenerarReporteJugadoresPDF(View):
    def get(self, request, *args, **kwargs):
        # Obtener todos los jugadores y calcular su edad
        jugadores = Jugador.objects.all().order_by('id')  # Ordenamos por ID
        for jugador in jugadores:
            jugador.edad = (datetime.date.today().year - jugador.fecha_nac.year)

        # Calcular el total de jugadores
        total_jugadores = jugadores.count()

        # Calcular el conteo de jugadores por posicion y rol
        conteo_por_puesto = Jugador.objects.values('puesto__puesto').annotate(total=Count('id'))

        # Datos para pasar al contexto
        context = {
            'jugadores': jugadores,
            'fecha': datetime.date.today(),
            'total_jugadores': total_jugadores,
            'conteo_por_puesto': conteo_por_puesto,  # Pasamos los datos por puesto
        }

        # Renderizar la plantilla HTML
        html = render_to_string('reporte_jugadores.html', context)

        # Crear la respuesta HTTP con tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_jugadores.pdf"'

        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response

# VISTA PARA GENERAR UN REPORTE DETALLADO DE UN JUGADOR EN PDF


class ReporteJugadorPDF(View):
    def get(self, request, pk, *args, **kwargs):
        # Obtener el jugador
        jugador = get_object_or_404(Jugador, pk=pk)

        # Calcular la edad del jugador
        hoy = date.today()
        edad = hoy.year - jugador.fecha_nac.year - ((hoy.month, hoy.day) < (jugador.fecha_nac.month, jugador.fecha_nac.day))

        # Construir URL absoluta para la foto del jugador
        foto_url = request.build_absolute_uri(jugador.foto.url) if jugador.foto else None

        # Contexto para el template
        context = {
            'detjugadores': jugador,
            'edad': edad,
            'foto_url': foto_url,  # Agregamos la URL completa de la foto
            'fecha': datetime.date.today()
        }

        # Renderizar el HTML
        template_path = 'reporte_detalle_jugador.html'
        html = render_to_string(template_path, context)

        # Configurar la respuesta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{jugador.nombre}_{jugador.apellido}.pdf"'

        # Generar el PDF usando xhtml2pdf
        pisa_status = CreatePDF(html, dest=response)

        # Verificar errores
        if pisa_status.err:
            return HttpResponse(f"Error al generar el PDF: {pisa_status.err}", content_type="text/plain")
        return response

class ReporteValoracionPDF(View):
    def get(self, request, *args, **kwargs):
        # Obtener el ID de la valoración desde la URL
        valoracion_id = self.kwargs.get('pk')

        # Obtener la valoración y sus detalles
        valoracion = get_object_or_404(Valoracion, id=valoracion_id)
        jugador = valoracion.jugador

        # Filtrar cualidades asociadas al puesto del jugador
        cualidades_asociadas = PuestoCualidad.objects.filter(puesto=jugador.puesto).select_related('cualidad')

        # Crear una lista dinámica de las cualidades con sus valores
        cualidades = []
        for puesto_cualidad in cualidades_asociadas:
            cualidad_nombre = puesto_cualidad.cualidad.cualidad.lower()
            valor_cualidad = getattr(valoracion, f"valoracion_{cualidad_nombre}", None)  # Obtener el valor dinámicamente
            cualidades.append({'nombre': puesto_cualidad.cualidad.cualidad, 'valor': valor_cualidad})

        # Contexto para la plantilla
        context = {
            'valoracion': valoracion,
            'jugador': jugador,
            'cualidades': cualidades,  # Solo las cualidades asociadas al puesto
            'estadisticas': valoracion.detalles.all(),  # Detalle de estadísticas
            'fecha': date.today(),
            'current_year': date.today().year,
        }

        # Renderizar la plantilla HTML
        html = render(request, 'reporte_valoraciones_detalle.html', context).content.decode('utf-8')

        # Crear el archivo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="valoracion_{valoracion.jugador.nombre}.pdf"'

        # Convertir HTML a PDF usando xhtml2pdf
        pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=response)

        # Manejar errores
        if pisa_status.err:
            return HttpResponse(f"Hubo un error al generar el PDF: {pisa_status.err}", status=400)

        return response
