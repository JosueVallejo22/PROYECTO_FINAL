from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from django.views.generic import * # type: ignore
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.forms import JugadorForm
from Aplicaciones.Login.models import Usuario
from Aplicaciones.Auditoria.utils import save_audit
from django.contrib import messages

##########################################################################################

def login_required(view_func):
    """Decorador para permitir solo el acceso a usuarios autenticados."""
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('Login:login_usuario')  # Redirige al login si no está autenticado
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@method_decorator(login_required, name='dispatch')
class MenuView(TemplateView):
    template_name = 'menu.html'

##########################################################################################

@method_decorator(login_required, name='dispatch')
class listjugadoresView(ListView):
    """vista para listar Jugadores"""
    model = Jugador
    template_name = 'listjugadores.html'
    context_object_name = 'listjugadores'
    queryset = Jugador.objects.filter(estado=True).order_by('nombre')


@method_decorator(login_required, name='dispatch')
class JugadoresDetailView(DetailView):
    """Vista para mostrar detalles de un jugador"""
    model = Jugador
    template_name = 'detalle_jugador.html'
    context_object_name = 'detjugadores'    


@method_decorator(login_required, name='dispatch')
class jugadoresCreateView(CreateView):
    """vista para crear un nuevo jugador"""
    template_name = 'form_jugador.html'
    model = Jugador
    form_class = JugadorForm
    success_url = reverse_lazy('core:listjugadores')

    def form_valid(self, form):
        jugador = form.save(commit=False)

        user_id = self.request.session.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        jugador.usuario = usuario.nombre_usuario

        jugador.save()

        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, 'Jugador registrado exitosamente.')
        return response
    

@method_decorator(login_required, name='dispatch')
class jugadoresUpdateView(UpdateView):
    """Vista para actualizar un jugador existente"""
    model = Jugador
    form_class = JugadorForm
    template_name = 'form_jugador.html'
    success_url = reverse_lazy('core:listjugadores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_editing'] = True
        return context
    
    def form_valid(self, form):
        jugador = form.save(commit=False)

        user_id = self.request.session.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        jugador.usuario = usuario.nombre_usuario

        jugador.save()
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'Jugador modificado exitosamente.')
        return response


@method_decorator(login_required, name='dispatch')
class ActivarInactivarJugador(View):
    """Vista para activar/inactivar un rol"""
    def get(self, request, pk):
        jugador = get_object_or_404(Jugador, pk=pk)
        jugador.estado = not jugador.estado
        
        user_id = self.request.session.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        jugador.usuario = usuario.nombre_usuario

        jugador.save()
        save_audit(self.request, jugador, action='E')
        messages.success(request, "Jugador eliminado exitosamente.")
        return redirect('core:listjugadores')

##########################################################################################