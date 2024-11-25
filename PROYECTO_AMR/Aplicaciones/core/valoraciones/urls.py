from django.urls import path
from Aplicaciones.core.valoraciones import views
from Aplicaciones.core.valoraciones.views import *


app_name = "valoraciones"

urlpatterns = [
    # Ruta para el módulo principal
    path('menu/valoraciones/', ModuloValoracionesView.as_view(), name='modulo_valoraciones'),

    # Ruta para el formulario de crear una nueva valoración
    path('menu/valoraciones/nueva/', CrearValoracionView.as_view(), name='crear_valoracion'),

    # Ruta para cargar cualidades de un jugador seleccionado (vista dinámica con JSON)
    path('cargar-cualidades/<int:jugador_id>/', CargarCualidadesView.as_view(), name='cargar_cualidades'),

    # Ruta para guardar la valoración en la base de datos
    path('menu/valoraciones/guardar/', GuardarValoracionView.as_view(), name='guardar_valoracion'),

    #Ruta de dashboards
    path('dashboards/', DashboardsView.as_view(), name='dashboards'),
    path('dashboards/<int:jugador_id>/evolucion-data/', ObtenerDatosValoracionView.as_view(), name='jugador-evolucion-data'),
    path('dashboards/distribucion/', ObtenerDatosDistribucionView.as_view(), name='api_distribucion'),
    path('dashboards/penales/', ObtenerDatosPenalesView.as_view(), name='api_penales'),
    path('dashboards/penales/<int:jugador_id>/', ObtenerDatosPenalesView.as_view(), name='api_penales_jugador'),
    ###############################################
    path('reporte-pdf/', views.generar_pdf_xhtml2pdf, name='reporte_pdf'),
    path('enviar-reporte-pdf/', views.enviar_pdf_correo, name='enviar_reporte_pdf'),

]