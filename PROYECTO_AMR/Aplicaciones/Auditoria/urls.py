from django.urls import path
from Aplicaciones.Auditoria.views import *

app_name = 'Auditoria'
urlpatterns = [
    path('reporte-usuarios/', GenerarReporteUsuariosPDF.as_view(), name='reporte_usuarios'),
    path('reporte-jugadores/', GenerarReporteJugadoresPDF.as_view(), name='reporte_jugadores'),
    path('reporte-jugador/<int:pk>/', ReporteJugadorPDF.as_view(), name='reporte_jugador'),
    path('valoraciones/<int:pk>/pdf/', ReporteValoracionPDF.as_view(), name='valoracion_pdf'),


]
