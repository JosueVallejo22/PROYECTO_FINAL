from django.shortcuts import render
from Aplicaciones.Login.models import *
from Aplicaciones.core.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import datetime
from django.views import *
from django.db.models import Count  # Importar Count para el conteo
from reportlab.pdfgen import canvas

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
        jugador = Jugador.objects.get(pk=pk)

        # Calcular la edad del jugador
        hoy = date.today()
        edad = hoy.year - jugador.fecha_nac.year - ((hoy.month, hoy.day) < (jugador.fecha_nac.month, jugador.fecha_nac.day))

        # Configurar la respuesta como PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{jugador.nombre}_{jugador.apellido}.pdf"'

        # Crear el PDF
        p = canvas.Canvas(response)

        # Título del reporte
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, 800, "Reporte Individual del Jugador")

        # Información del jugador
        p.setFont("Helvetica", 12)
        p.drawString(50, 750, f"Nombre: {jugador.nombre}")
        p.drawString(50, 730, f"Apellido: {jugador.apellido}")
        p.drawString(50, 710, f"Nacionalidad: {jugador.pais.pais}")
        p.drawString(50, 690, f"Puesto: {jugador.puesto.puesto}")
        p.drawString(50, 670, f"Fecha de Nacimiento: {jugador.fecha_nac.strftime('%d/%m/%Y')}")
        p.drawString(50, 650, f"Edad: {edad} años")
        p.drawString(50, 630, f"Correo: {jugador.correo}")
        p.drawString(50, 610, f"Pierna Hábil: {jugador.get_pierna_habil_display()}")
        p.drawString(50, 590, f"Altura: {jugador.altura} cm")
        p.drawString(50, 570, f"Peso: {jugador.peso} kg")
        p.drawString(50, 550, f"Estado: {'Activo' if jugador.estado else 'Inactivo'}")

        # Información de auditoría
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, 520, "Información de Auditoría:")
        p.setFont("Helvetica", 12)
        p.drawString(50, 500, f"Usuario: {jugador.usuario}")
        p.drawString(50, 480, f"Fecha de Creación: {jugador.fecha_creacion.strftime('%d/%m/%Y %H:%M')}")
        p.drawString(50, 460, f"Última Actualización: {jugador.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')}")

        # Finalizar el documento
        p.showPage()
        p.save()
        return response
