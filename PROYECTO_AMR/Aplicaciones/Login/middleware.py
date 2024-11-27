class SessionUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el usuario está autenticado
        if request.session.get('user_id'):
            # Actualizar el tiempo de expiración de la sesión
            request.session.set_expiry(600)  # 10 minutos, o el tiempo que prefieras
            
        response = self.get_response(request)
        return response

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class CambioContrasenaMiddleware:
    """Middleware para verificar si el usuario debe cambiar su contraseña"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Excluir las rutas relacionadas con el login y el cambio de contraseña
        excluded_urls = [
            reverse('Login:login_usuario'),
            reverse('Login:cambiar_contrasena'),  # Ajusta este nombre si es necesario
            reverse('Login:solicitar_restablecimiento'),  # Ajusta este nombre si es necesario
            reverse('Login:verifica_correo'),
            reverse('Login:form_nueva_clave'),
            reverse('Login:restablecimiento_exitoso'),
            reverse('Login:logout_usuario'),
        ]

        # Verificar si el usuario está autenticado y no está en las URLs excluidas
        if request.session.get('user_id'):
            usuario_id = request.session.get('user_id')
            from Aplicaciones.Login.models import Usuario  # Importa tu modelo de usuario
            usuario = Usuario.objects.get(id=usuario_id)

            if usuario.cambio_pass and request.path not in excluded_urls:
                # Redirigir al formulario de cambio de contraseña
                messages.warning(request, "Debes cambiar tu contraseña antes de continuar.")
                return redirect('Login:cambiar_contrasena')  # Ruta al formulario de cambio de contraseña

        response = self.get_response(request)
        return response
