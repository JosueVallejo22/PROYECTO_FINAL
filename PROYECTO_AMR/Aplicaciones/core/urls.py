from django.urls import path # type: ignore
from Aplicaciones.core.views import *
from PROYECTO_AMR import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # type: ignore
from django.conf.urls.static import static # type: ignore

app_name = 'core'

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('listjugadores/', listjugadoresView.as_view(), name='listjugadores'),
    path('detjugadores/<int:pk>/', JugadoresDetailView.as_view(), name='detjugadores'),
    path('crearjugador/', jugadoresCreateView.as_view(),name='crearjugador'),
    path('editjugadores/<int:pk>', jugadoresUpdateView.as_view(), name='editjugadores'),
    path('eliminar/<int:pk>/', ActivarInactivarJugador.as_view(), name='eliminar_jugador'),

    path('comparar/', CompararJugadoresView.as_view(), name='comparar_jugadores'),
    path('api/jugadores/', BuscarJugadoresView.as_view(), name='buscar_jugadores'),
    path('api/comparar/', CompararJugadoresStatsView.as_view(), name='comparar_jugadores_stats'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)