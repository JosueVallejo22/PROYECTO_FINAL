from django.urls import path
from Aplicaciones.core.valoraciones.views import *

app_name = 'valoraciones'

urlpatterns = [
    path('modulo_valoraciones/', ValoracionesView.as_view(), name='valoraciones'),
    path('form_valoraciones', FormularioValoracionView.as_view(), name='formulario_valoraciones'),

]