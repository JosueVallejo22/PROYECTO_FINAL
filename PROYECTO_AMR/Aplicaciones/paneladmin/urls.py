from django.urls import path
from Aplicaciones.paneladmin.views import *

app_name = 'paneladmin'

urlpatterns = [
    #MENU
    path('menu_admin/', MenuAdmin.as_view(), name='menu_admin'),
    path('menu_modulo_usuarios/', MenuModUsuarios.as_view(), name='menu_modulo_usuarios'),
    #MANTENIMIENTO ROLES
    path('mantenimiento_roles/', RolListView.as_view(), name='mantenimiento_roles'),
    path('crear_rol/', RolCreateView.as_view(), name='crear_rol'),
    path('editar_rol/<int:pk>/', RolUpdateView.as_view(), name='editar_rol'),
    path('activar-inactivar-rol/<int:pk>/',ActivarInactivarRol.as_view(),name='activar-inactivar-rol'),
    #MANTENIMIENTO USUARIOS
    path('mantenimiento_usuarios/', UsuarioListView.as_view(), name='mantenimiento_usuarios'),
    path('usuario/<int:pk>/', UsuarioDetailView.as_view(), name='detalle_usuario'),
    path('crear_usuario/', CrearUsuarios.as_view(), name='crear_usuario'),
    path('editar_usuario/<int:pk>', ActualizarUsuario.as_view(), name='editar_usuario'),
    path('activar-inactivar-usuario/<int:pk>', ActivarInactivarUsuario.as_view(), name='activar-inactivar-usuario'),
]