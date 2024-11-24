from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from Aplicaciones.Login.models import Usuario, Rol
from Aplicaciones.paneladmin.forms import RolForm, UsuarioForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from Aplicaciones.Auditoria.utils import save_audit
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings
from django.core.mail import EmailMessage

# Decorador para verificar si el usuario es administrador
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('Login:login_usuario')
        
        usuario = get_object_or_404(Usuario, id=user_id)
        if usuario.rol.rol != "ADMINISTRADOR":
            return render(request, 'inaccesible.html', status=403)
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

##########################################################################################
@method_decorator(admin_required, name='dispatch')
class MenuAdmin(View):
    """Vista para el menú de administración"""
    
    def get(self, request):
        usuario_logueado = get_object_or_404(Usuario, id=request.session['user_id'])
        return render(request, 'menu_admin.html', {'usuario': usuario_logueado})

@method_decorator(admin_required, name='dispatch')
class MenuModUsuarios(View):
    """Vista para el módulo de usuarios"""
    def get(self, request):
        usuario_logueado = get_object_or_404(Usuario, id=request.session['user_id'])
        return render(request, 'menu_modulo_usuarios.html', {'usuario': usuario_logueado})

@method_decorator(admin_required, name='dispatch')
class RolListView(ListView):
    """Vista para listar roles con búsqueda"""
    model = Rol
    template_name = 'mantenimiento_roles.html'
    context_object_name = 'roles'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Obtiene el valor de búsqueda
        queryset = Rol.objects.all().order_by('rol', '-estado')  # Ordena por rol y estado
        if query:
            queryset = queryset.filter(
                Q(rol__icontains=query)  # Busca por rol
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q', '')  # Valor del campo de búsqueda
        context['clear_url'] = self.request.path  # URL para el botón "Limpiar"
        return context


    
@method_decorator(admin_required, name='dispatch')
class RolCreateView(CreateView):
    """Vista para crear un nuevo rol"""
    model = Rol
    form_class = RolForm
    template_name = 'mantenimiento_roles.html'
    success_url = reverse_lazy('paneladmin:mantenimiento_roles')

    def form_valid(self, form):
        # Guardar el rol y agregar el mensaje de éxito
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, 'Rol creado exitosamente.')
        return response

    def form_invalid(self, form):
        # Agregar los errores del formulario como mensajes
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        # Redirigir al listado de roles
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        # Agregar los roles al contexto para el listado
        context = super().get_context_data(**kwargs)
        context['roles'] = Rol.objects.all().order_by('-estado')
        return context

@method_decorator(admin_required, name='dispatch')
class RolUpdateView(UpdateView):
    """Vista para actualizar un rol existente"""
    model = Rol
    form_class = RolForm
    template_name = 'mantenimiento_roles.html'
    success_url = reverse_lazy('paneladmin:mantenimiento_roles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Rol.objects.all().order_by('-estado')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'Rol Modificado exitosamente.')
        return response

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarRol(View):
    """Vista para activar/inactivar un rol"""
    def get(self, request, pk):
        rol = get_object_or_404(Rol, pk=pk)
        rol.estado = not rol.estado
        rol.save()
        save_audit(self.request, rol, action='M')
        messages.success(request, "Estado del rol actualizado exitosamente.")
        return redirect('paneladmin:mantenimiento_roles')

############################################################################################

@method_decorator(admin_required, name='dispatch')
class UsuarioListView(ListView):
    """Vista para listar usuarios con filtros y búsqueda"""
    model = Usuario
    template_name = 'mantenimiento_usuario.html'
    context_object_name = 'usuarios'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')  # Búsqueda por nombre o apellido
        rol_filter = self.request.GET.get('rol', '')  # Filtro por rol

        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(apellido__icontains=search_query)
            )

        if rol_filter:
            queryset = queryset.filter(rol__id=rol_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Rol.objects.filter(estado=True).order_by('rol')
        context['rol_selected'] = self.request.GET.get('rol', '')
        context['search'] = self.request.GET.get('search', '')
        context['clear_url'] = self.request.path

        # Obtener detalles del usuario si se proporciona el parámetro `detalle`
        detalle_id = self.request.GET.get('detalle')
        if detalle_id:
            context['detalle_usuario'] = Usuario.objects.filter(id=detalle_id).first()

        return context




@method_decorator(admin_required, name='dispatch')
class UsuarioDetailView(DetailView):
    """Vista para mostrar detalles de un usuario"""
    model = Usuario
    template_name = 'mantenimiento_usuario.html'
    context_object_name = 'usuario'

@method_decorator(admin_required, name='dispatch')
class CrearUsuarios(CreateView):
    """Vista para crear un nuevo usuario"""
    model = Usuario
    form_class = UsuarioForm
    template_name = 'form_usuario.html'
    success_url = reverse_lazy('paneladmin:mantenimiento_usuarios')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.estado = True  # Activo por defecto
        clave_temporal = usuario.generar_contrasena_temporal()
        usuario.clave = clave_temporal
        usuario.save()
        save_audit(self.request, usuario, action='A')
        self.enviar_correo_bienvenida(usuario.correo, usuario.nombre_usuario, clave_temporal)
        messages.success(self.request, 'Usuario creado exitosamente.')
        return super().form_valid(form)



    def enviar_correo_bienvenida(self, correo, nombre_usuario, clave_temporal):
        """Función para enviar correo de bienvenida al nuevo usuario"""
        # Renderizar el correo con la plantilla
        mensaje_html = render_to_string('correo_bienvenida.html', {
            'nombre_usuario': nombre_usuario,
            'clave': clave_temporal,
            'login_url': settings.LOGIN_URL,  # Define la URL de inicio de sesión en settings.py
            'current_year': now().year
        })
        # Crear y enviar el correo
        email = EmailMessage(
            subject="Bienvenido/a a la Plataforma",  # Asunto
            body=mensaje_html,  # Cuerpo del correo
            from_email=settings.EMAIL_HOST_USER,  # Dirección de correo del remitente
            to=[correo],  # Dirección de correo del destinatario
        )
        email.content_subtype = 'html'  # Establecer el formato del correo a HTML
        email.send(fail_silently=False)



@method_decorator(admin_required, name='dispatch')
class ActualizarUsuario(UpdateView):
    """Vista para actualizar un usuario existente"""
    model = Usuario
    form_class = UsuarioForm
    template_name = 'form_usuario.html'
    success_url = reverse_lazy('paneladmin:mantenimiento_usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'Usuario modificado exitosamente.')
        return response

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarUsuario(View):
    """Vista para activar/inactivar un usuario"""
    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)

        # Obtener el ID del usuario en sesión
        user_id_sesion = request.session.get('user_id')

        # Comprobar si el usuario en sesión es el mismo que se intenta inactivar
        if usuario.id == user_id_sesion:
            messages.error(request, "No puedes inactivar tu propia cuenta.")
            return redirect('paneladmin:mantenimiento_usuarios')

        usuario.estado = not usuario.estado
        usuario.save()
        save_audit(self.request, usuario, action='M')
        messages.success(request, "Estado del usuario actualizado exitosamente.")
        return redirect('paneladmin:mantenimiento_usuarios')


# Vista genérica para la página de acceso denegado
class InaccesibleView(View):
    template_name = 'inaccesible.html'

    def get(self, request):
        return render(request, self.template_name)
