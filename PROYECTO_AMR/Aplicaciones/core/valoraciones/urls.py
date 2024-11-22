from django.urls import path
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
    path('jugador/<int:jugador_id>/evolucion-data/', ObtenerDatosValoracionView.as_view(), name='jugador-evolucion-data'),

]