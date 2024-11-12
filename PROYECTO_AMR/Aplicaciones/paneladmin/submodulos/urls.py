from django.urls import path
from Aplicaciones.paneladmin.submodulos.views import *

app_name = 'submodulos'

urlpatterns = [
    #MENU SUBMODULOS
    path('menu_submodulos/', MenuSubmodulos.as_view(), name= 'menu_submodulos'),
    #MANTENIMIENTO PAISES
    path('mantenimiento_paises/', PaisListView.as_view(), name= 'mantenimiento_paises'),
    path('registrar_pais/', PaisCreateView.as_view(), name= 'registrar_pais'),
    path('editar_pais/<int:pk>/', PaisUpdateView.as_view(), name= 'editar_pais'),
    path('activar-inactivar-pais/<int:pk>/', ActivarInactivarPais.as_view(), name= 'activar-inactivar-pais'),
    #MANTENIMIENTO CUALIDADES
    path('mantenimiento_cualidades/', CualidadListView.as_view(), name='mantenimiento_cualidades'),
    path('registrar_cualidad/', CualidadCreateView.as_view(), name='registrar_cualidad'),
    path('editar_cualidad/<int:pk>/',CualidadUpdateView.as_view(), name='editar_cualidad'),
    path('activar-inactivar-cualidad/<int:pk>/',ActivarInactivarCualidad.as_view(), name='activar-inactivar-cualidad'),
    #MANTENIMIENTO ESTADISTICAS
    path('mantenimiento_estadisticas/', EstadisticasListView.as_view(), name='mantenimiento_estadisticas'),
    path('registrar_estadistica/', EstadisticasCreateView.as_view(), name='registrar_estadistica'),
    path('editar_estadistica/<int:pk>/',EstadisticaUpdateView.as_view(), name='editar_estadistica'),
    path('activar-inactivar-estadistica/<int:pk>/',ActivarInactivarEstadistica.as_view(), name='activar-inactivar-estadistica'),
    #MANTENIMIENTO POSICIONES
    path('mantenimiento_posicion/', PosicionListView.as_view(), name='mantenimiento_posicion'),
    path('registrar_posicion/', PosicionCreateView.as_view(), name='registrar_posicion'),
    path('editar_posicion/<int:pk>/',PosicionUpdateView.as_view(), name='editar_posicion'),
    path('activar-inactivar-posicion/<int:pk>/',ActivarInactivarPosicion.as_view(), name='activar-inactivar-posicion'),
    #MANTENIMIENTO PUESTO
    path('mantenimiento_puesto/', PuestoListView.as_view(), name='mantenimiento_puesto'),
    path('registrar_puesto/', PuestoCreateView.as_view(), name='registrar_puesto'),
    path('editar_puesto/<int:pk>/',PuestoUpdateView.as_view(), name='editar_puesto'),
    path('activar-inactivar-puesto/<int:pk>/',ActivarInactivarPuesto.as_view(), name='activar-inactivar-puesto'),
    #CUALIDAD PUESTO
    path('cualidad_puesto/', PuestoCualidadListView.as_view(), name='mantenimiento_puesto_cualidad'),
    path('cualidad_puesto/crear/', PuestoCualidadCreateView.as_view(), name='registrar_puesto_cualidad'),
    path('cualidad_puesto/editar/<int:pk>/', PuestoCualidadUpdateView.as_view(), name='editar_puesto_cualidad'),
    path('cualidad_puesto/activar-inactivar/<int:pk>/', ActivarInactivarPuestoCualidad.as_view(), name='activar-inactivar-puesto-cualidad'),
    #JUGADORES ADMIN
    path('lista_jugadores/', ListarJugador.as_view(), name='listar_jugador_admin'),
    path('registrar_jugador/', JugadorCreateView.as_view(), name='crear_jugador_admin'),
    path('detalle_jugadores/<int:pk>/', DetalleJugadores.as_view(), name='detalle_jugador_admin'),
    path('editar_jugadores/<int:pk>/', JugadorUpdateView.as_view(), name='editar_jugador_admin'),
    path('act-inact-jugadores/<int:pk>/', ActivarInactivarJugadorAd.as_view(), name='act-inact-jugadores-admin'),
]
