from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView # type: ignore
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.forms import JugadorForm
from Aplicaciones.Login.models import Usuario

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)  # Obtener el usuario logueado
        context['usuario'] = usuario  # Pasar el usuario al contexto
        return context


##########################################################################################

@method_decorator(login_required, name='dispatch')
class listjugadoresView(ListView):
    """vista para listar Jugadores"""
    model = Jugador
    template_name = 'listjugadores.html'
    context_object_name = 'listjugadores'
    queryset = Jugador.objects.all().order_by('nombre')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el usuario logueado y agregarlo al contexto
        user_id = self.request.session.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        context['usuario'] = usuario
        return context
    

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

@method_decorator(login_required, name='dispatch')   
class JugadoresDeleteView(DeleteView):
    model = Jugador
    success_url = reverse_lazy('core:listjugadores')

##########################################################################################
@method_decorator(login_required, name='dispatch')
class listvaloracionesView(TemplateView):
    template_name = 'listvaloraciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el usuario logueado y agregarlo al contexto
        user_id = self.request.session.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        context['usuario'] = usuario
        
        return context
