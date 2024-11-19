from django.urls import path
from Aplicaciones.core.valoraciones.views import *

app_name = "valoraciones"

urlpatterns = [
    path('menu/valoraciones/', ModuloValoracionesView.as_view(), name='modulo_valoraciones'),
    # Cambié la vista de 'GenerarValoracionView' a 'CrearValoracionView'
    path('menu/valoraciones/nueva/', CrearValoracionView.as_view(), name='crear_valoracion'),
    path('cargar-cualidades/<int:jugador_id>/', CargarCualidadesView.as_view(), name='cargar_cualidades'),
]
