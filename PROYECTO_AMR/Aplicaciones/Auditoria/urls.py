from django.urls import path
from Aplicaciones.Auditoria.views import *

app_name = 'Auditoria'
urlpatterns = [
    path('reporte-usuarios/', GenerarReporteUsuariosPDF.as_view(), name='reporte_usuarios'),
]
