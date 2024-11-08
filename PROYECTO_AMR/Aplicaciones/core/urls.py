from django.urls import path
from Aplicaciones.core.views import *
from PROYECTO_AMR import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('listjugadores/', listjugadoresView.as_view(), name='listjugadores'),
    path('detjugadores/<int:pk>/', JugadoresDetailView.as_view(), name='detjugadores'),
    path('crearjugador/', jugadoresCreateView.as_view(),name='crearjugador'),
    path('editjugadores/<int:pk>', jugadoresUpdateView.as_view(), name='editjugadores'),

    
    path('listvaloraciones/', listvaloracionesView.as_view(), name='listvaloraciones'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)