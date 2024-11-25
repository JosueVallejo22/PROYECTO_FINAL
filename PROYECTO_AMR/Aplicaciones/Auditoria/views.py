from django.shortcuts import render
from Aplicaciones.Login.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import datetime
from django.views import *

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

        # Datos para pasar al contexto
        context = {
            'usuarios': usuarios,
            'fecha': datetime.date.today(),
            'total_usuarios': total_usuarios,  # Pasamos el total de usuarios
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