from django.http import HttpResponse
from wkhtmltopdf.views import PDFTemplateResponse

def prueba_pdf(request):
    # Datos que quieres pasar al HTML
    context = {
        'titulo': 'Prueba de Generación de PDF',
        'contenido': 'Este PDF fue generado con wkhtmltopdf en Django.',
    }

    # Crear el PDF
    response = PDFTemplateResponse(
        request=request,
        template='pruebaPDF.html',  # Asegúrate de crear esta plantilla
        context=context,
        filename="prueba.pdf",  # Nombre del archivo generado
        show_content_in_browser=False,  # Cambia a True si prefieres mostrarlo en el navegador
        cmd_options={
            'encoding': 'utf-8',  # Soporte para caracteres especiales
            'margin-top': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm',
            'margin-right': '10mm',
        }
    )
    return response
