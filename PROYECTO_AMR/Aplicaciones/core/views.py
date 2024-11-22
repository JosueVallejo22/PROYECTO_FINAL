from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from django.views.generic import * # type: ignore
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.forms import JugadorForm
from Aplicaciones.Login.models import Usuario
from Aplicaciones.Auditoria.utils import save_audit
from django.contrib import messages
from Aplicaciones.paneladmin.submodulos.models import Puesto
from django.http import JsonResponse
from Aplicaciones.paneladmin.submodulos.models import *
from Aplicaciones.core.valoraciones.models import *
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

from django.db.models import Q
from django.core.paginator import Paginator

@method_decorator(login_required, name='dispatch')
class listjugadoresView(ListView):
    """Vista para listar Jugadores con filtros, búsqueda y paginación"""
    model = Jugador
    template_name = 'listjugadores.html'
    context_object_name = 'listjugadores'
    paginate_by = 5  # Número de jugadores por página

    def get_queryset(self):
        """Filtrar jugadores según búsqueda y puesto"""
        queryset = self.model.objects.filter(estado=True)

        # Obtener parámetros de búsqueda
        search_query = self.request.GET.get('search', '').strip()
        puesto_filter = self.request.GET.get('puesto', '')

        # Filtro de búsqueda por nombre o apellido
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) | Q(apellido__icontains=search_query)
            )

        # Filtro por puesto
        if puesto_filter:
            queryset = queryset.filter(puesto__id=puesto_filter)

        # Ordenar alfabéticamente por nombre
        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        """Agregar datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)

        # Obtener la lista de puestos para el filtro
        context['puestos'] = Puesto.objects.filter(estado=True).order_by('puesto')

        # Agregar parámetros de búsqueda actuales al contexto
        context['search_query'] = self.request.GET.get('search', '')
        context['puesto_filter'] = self.request.GET.get('puesto', '')

        return context



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
class CompararJugadoresView(TemplateView):
    template_name = 'comparar_jugadores.html'

class BuscarJugadoresView(View):
    def get(self, request, *args, **kwargs):
        """
        Devuelve una lista de valoraciones de jugadores filtradas por un término de búsqueda.
        """
        search_term = request.GET.get("q", "").strip()  # Término de búsqueda ingresado por el usuario
        valoraciones = Valoracion.objects.filter(
            Q(jugador__estado=True) &  # Filtrar solo jugadores activos
            (Q(jugador__nombre__icontains=search_term) | Q(jugador__apellido__icontains=search_term))  # Buscar coincidencias
        ).select_related('jugador')

        # Formateamos los datos para enviarlos al frontend
        data = [
            {
                "id": valoracion.id,  # ID único de la valoración
                "nombre": f"{valoracion.jugador.nombre} {valoracion.jugador.apellido}",
                "puesto": valoracion.jugador.puesto.abreviatura if valoracion.jugador.puesto else "N/A",
                "foto": valoracion.jugador.foto.url if valoracion.jugador.foto else "/static/img/default-player.png",
            }
            for valoracion in valoraciones
        ]

        return JsonResponse({"jugadores": data})



class CompararJugadoresStatsView(View):
    def get(self, request, *args, **kwargs):
        """
        Devuelve las estadísticas de los jugadores seleccionados, respetando el orden recibido.
        """
        jugadores_ids = request.GET.get("valoraciones")  # Recibe el parámetro como cadena
        if not jugadores_ids:
            return JsonResponse({"error": "No se proporcionaron IDs de jugadores."}, status=400)

        # Convertir los IDs a una lista de enteros
        try:
            jugadores_ids = [int(id) for id in jugadores_ids.split(",")]
        except ValueError:
            return JsonResponse({"error": "IDs de jugadores inválidos."}, status=400)

        # Buscar valoraciones activas y respetar el orden recibido
        valoraciones = list(Valoracion.objects.filter(id__in=jugadores_ids).select_related("jugador"))
        valoraciones.sort(key=lambda x: jugadores_ids.index(x.id))  # Ordenar según el orden de los IDs recibidos

        data = []
        for valoracion in valoraciones:
            jugador = valoracion.jugador
            cualidades = [
                {"nombre": pc.cualidad.cualidad, "valor": getattr(valoracion, f"valoracion_{pc.cualidad.cualidad.lower()}", 0)}
                for pc in PuestoCualidad.objects.filter(puesto=jugador.puesto, estado=True)
            ]

            jugador_data = {
                "id": valoracion.id,
                "nombre": f"{jugador.nombre} {jugador.apellido}",
                "puesto": jugador.puesto.abreviatura,
                "foto": jugador.foto.url if jugador.foto else None,
                "cualidades": cualidades,
            }

            data.append(jugador_data)

        return JsonResponse({"jugadores": data})
