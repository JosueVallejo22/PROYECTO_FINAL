import re
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views import View
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from Aplicaciones.Login.forms import *
from Aplicaciones.Login.models import Usuario
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from Aplicaciones.core.views import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now

# Vistas de Restablecimiento de Contraseña
def verifica_correo(request):
    return render(request, 'verifica_correo.html')

def restablecimiento_exitoso(request):
    return render(request, 'restablecimiento_exitoso.html')

def solicitar_restablecimiento(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return render(request, 'form_correo.html', {
                'error': 'El correo electrónico no está registrado en el sistema.'
            })

        # Generar y guardar el token
        reset_token = get_random_string(length=50)
        usuario.reset_token = reset_token
        usuario.reset_token_used = False
        usuario.save()

        reset_url = request.build_absolute_uri(reverse('Login:form_nueva_clave') + f'?token={reset_token}')
        email_html_content = render_to_string('plantilla_correo.html', {
            'url_restablecimiento': reset_url,
            'nombre': usuario.nombre,
            'current_year': now().year

            
        })

        email = EmailMultiAlternatives(
            subject="Restablecimiento de Contraseña",
            body="Por favor haz clic en el enlace para restablecer tu contraseña.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[correo],
        )
        email.attach_alternative(email_html_content, "text/html")
        email.send()

        return redirect('Login:verifica_correo')

    return render(request, 'form_correo.html')

def form_nueva_clave(request):
    token = request.GET.get('token')
    if not token:
        raise Http404("Página no encontrada.")

    usuario = get_object_or_404(Usuario, reset_token=token, reset_token_used=False)

    if request.method == 'POST':
        form = NuevaClaveForm(request.POST)
        if form.is_valid():
            nueva_clave = form.cleaned_data['nueva_clave']
            confirmar_clave = form.cleaned_data['confirmar_clave']

            if nueva_clave != confirmar_clave:
                messages.error(request, "Las contraseñas no coinciden.")
            elif not validar_contrasena(nueva_clave):
                messages.error(request, "La contraseña debe contener al menos una letra mayúscula, una minúscula, un número y un carácter especial.")
            else:
                usuario.clave = nueva_clave
                usuario.reset_token_used = True
                usuario.reset_token = None
                usuario.save()
                messages.success(request, 'Contraseña cambiada exitosamente.')
                return redirect('Login:restablecimiento_exitoso')
        return render(request, 'form_nueva_clave.html', {'form': form, 'token': token})

    form = NuevaClaveForm()
    return render(request, 'form_nueva_clave.html', {'form': form, 'token': token})

def validar_contrasena(contrasena):
    """Valida que la contraseña contenga al menos una mayúscula, una minúscula, un número y un carácter especial."""
    return all([
        re.search(r'[A-Z]', contrasena),  # Al menos una letra mayúscula
        re.search(r'[a-z]', contrasena),  # Al menos una letra minúscula
        re.search(r'[0-9]', contrasena),  # Al menos un número
        re.search(r'[!@#$%^&*(),.?":{}|<>-_]', contrasena)  # Al menos un carácter especial
    ])
#####################
#vistas para cambiar contrasena dentro del aplicativo

@method_decorator(login_required, name='dispatch')
class CambiarContrasenaView(View):
    form_class = CambioContrasenaForm
    template_name = 'cambiar_contrasena.html'  # Crea esta plantilla

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            contrasena_actual = form.cleaned_data['contrasena_actual']
            nueva_contrasena = form.cleaned_data['nueva_contrasena']

            usuario_id = request.session.get('user_id')
            if usuario_id:
                usuario = Usuario.objects.get(id=usuario_id)

                if not usuario.check_password(contrasena_actual):
                    messages.error(request, "La contraseña actual es incorrecta.")
                else:
                    usuario.clave = nueva_contrasena
                    usuario.save()
                    messages.success(request, "Contraseña cambiada exitosamente.")
                    return redirect('Login:login_usuario')  # Redirige a donde desees

        return render(request, self.template_name, {'form': form})



# Vistas de Login
class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        # Redirigir a usuarios ya autenticados
        user_id = request.session.get('user_id')
        if user_id:
            usuario = Usuario.objects.get(id=user_id)
            if usuario.rol.estado:  # Verificar que el rol del usuario esté activo
                rol_usuario = usuario.rol.rol
                return redirect('paneladmin:menu_admin' if rol_usuario == "ADMINISTRADOR" else 'core:menu')
            else:
                # Si el rol está inactivo, cerrar sesión y mostrar mensaje
                request.session.flush()
                messages.error(request, 'Su rol se encuentra inactivo. Comuníquese con el administrador.')
                return redirect('login')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            clave = form.cleaned_data['clave']

            try:
                usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)

                # Verificar si el usuario está inactivo
                if not usuario.estado:
                    form.add_error(None, 'ESTE USUARIO SE ENCUENTRA INACTIVO.')
                # Verificar si el rol del usuario está inactivo
                elif not usuario.rol.estado:
                    form.add_error(None, 'SU ROL ESTÁ INACTIVO. CONTACTE AL ADMINISTRADOR.')
                # Verificar las credenciales
                elif usuario.check_password(clave):
                    # Guardar el ID del usuario en la sesión y registrar el inicio de sesión
                    request.session['user_id'] = usuario.id
                    usuario.ultimo_inicio_sesion = timezone.now()
                    usuario.save()
                    return redirect('paneladmin:menu_admin' if usuario.rol.rol == "ADMINISTRADOR" else 'core:menu')
                else:
                    form.add_error(None, 'LAS CREDENCIALES INGRESADAS SON INCORRECTAS.')
            except Usuario.DoesNotExist:
                form.add_error(None, 'USUARIO NO REGISTRADO.')

        return render(request, self.template_name, {'form': form})



# Cierre de Sesión
def logout_view(request):
    del request.session['user_id']
    return redirect('Login:login_usuario')
