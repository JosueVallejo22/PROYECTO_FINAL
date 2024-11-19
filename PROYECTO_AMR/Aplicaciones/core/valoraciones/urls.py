from django.urls import path
from Aplicaciones.core.valoraciones.views import *

app_name = "valoraciones"

urlpatterns = [
    path('menu/valoraciones/', ModuloValoracionesView.as_view(), name='modulo_valoraciones'),
    path('menu/valoraciones/nueva/', GenerarValoracionView.as_view(), name='generar_valoracion'),
    path('cargar-cualidades/<int:jugador_id>/', CargarCualidadesView.as_view(), name='cargar_cualidades'),
]
