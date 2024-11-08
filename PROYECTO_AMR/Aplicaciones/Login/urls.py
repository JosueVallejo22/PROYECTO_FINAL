from django.urls import path
from .views import *

app_name = 'Login'

urlpatterns = [
    path('', LoginView.as_view(), name='login_usuario'),
    path('cerrar_sesion/', logout_view, name='logout_usuario'),
    path('cambiar_contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    path('solicitar-restablecimiento/', solicitar_restablecimiento, name='solicitar_restablecimiento'),
    path('verifica_correo/', verifica_correo, name='verifica_correo'),
    path('nueva-clave/', form_nueva_clave, name='form_nueva_clave'),
    path('restablecimiento-exitoso/', restablecimiento_exitoso, name='restablecimiento_exitoso'),
]