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

from django.db.models import OuterRef, Subquery, Exists

from django.db.models import OuterRef, Subquery, Exists, Q
from django.http import JsonResponse
from django.views import View

class JugadoresConValoracionView(View):
    """
    Vista para obtener jugadores activos que tienen al menos una valoración
    y coinciden con el término de búsqueda.
    """
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("q", "").strip()  # Obtén el término de búsqueda

        # Subquery para verificar si hay al menos una valoración
        valoraciones_subquery = Valoracion.objects.filter(jugador=OuterRef('pk'))

        # Subquery para obtener la última valoración
        ultima_valoracion = valoraciones_subquery.order_by('-id')

        # Filtrar jugadores activos y coincidentes con el término de búsqueda
        jugadores = (
            Jugador.objects.filter(
                estado=True  # Solo jugadores activos
            )
            .filter(
                Q(nombre__icontains=search_query) | Q(apellido__icontains=search_query)  # Búsqueda por nombre o apellido
            )
            .annotate(
                tiene_valoracion=Exists(valoraciones_subquery)  # Anota si tienen valoraciones
            )
            .filter(
                tiene_valoracion=True  # Filtra jugadores con al menos una valoración
            )
            .annotate(
                ultima_valoracion_total=Subquery(ultima_valoracion.values('valoracion_total')[:1]),
                ultima_valoracion_tiro=Subquery(ultima_valoracion.values('valoracion_tiro')[:1]),
                ultima_valoracion_pase=Subquery(ultima_valoracion.values('valoracion_pase')[:1]),
                ultima_valoracion_velocidad=Subquery(ultima_valoracion.values('valoracion_velocidad')[:1]),
                ultima_valoracion_regate=Subquery(ultima_valoracion.values('valoracion_regate')[:1]),
                ultima_valoracion_defensa=Subquery(ultima_valoracion.values('valoracion_defensa')[:1]),
                ultima_valoracion_fisico=Subquery(ultima_valoracion.values('valoracion_fisico')[:1]),
                ultima_valoracion_reflejos=Subquery(ultima_valoracion.values('valoracion_reflejos')[:1]),
                ultima_valoracion_manejo=Subquery(ultima_valoracion.values('valoracion_manejo')[:1]),
                ultima_valoracion_saque=Subquery(ultima_valoracion.values('valoracion_saque')[:1]),
            )
        )

        # Formatear los datos para enviarlos al frontend
        data = [
            {
                "id": jugador.id,
                "nombre": f"{jugador.nombre} {jugador.apellido}",
                "puesto": jugador.puesto.abreviatura if jugador.puesto else "N/A",
                "foto": jugador.foto.url if jugador.foto else "/static/img/default-player.png",
                "ultima_valoracion": {
                    "total": jugador.ultima_valoracion_total,
                    "tiro": jugador.ultima_valoracion_tiro,
                    "pase": jugador.ultima_valoracion_pase,
                    "velocidad": jugador.ultima_valoracion_velocidad,
                    "regate": jugador.ultima_valoracion_regate,
                    "defensa": jugador.ultima_valoracion_defensa,
                    "fisico": jugador.ultima_valoracion_fisico,
                    "reflejos": jugador.ultima_valoracion_reflejos,
                    "manejo": jugador.ultima_valoracion_manejo,
                    "saque": jugador.ultima_valoracion_saque,
                },
            }
            for jugador in jugadores
        ]

        return JsonResponse({"jugadores": data})


class CompararValoresJugadoresView(View):
    """
    API para obtener las cualidades de comparación entre dos jugadores.
    """
    def get(self, request, *args, **kwargs):
        # Obtener IDs de los jugadores seleccionados
        jugador1_id = request.GET.get("jugador1")
        jugador2_id = request.GET.get("jugador2")

        if not jugador1_id or not jugador2_id:
            return JsonResponse({"error": "Faltan IDs de los jugadores para la comparación."}, status=400)

        # Obtener las valoraciones más recientes de cada jugador
        valoracion1 = Valoracion.objects.filter(jugador_id=jugador1_id).order_by('-id').first()
        valoracion2 = Valoracion.objects.filter(jugador_id=jugador2_id).order_by('-id').first()

        if not valoracion1 or not valoracion2:
            return JsonResponse({"error": "No se encontraron valoraciones para uno o ambos jugadores."}, status=404)

        # Obtener cualidades asociadas a los puestos de ambos jugadores
        puesto1_cualidades = PuestoCualidad.objects.filter(puesto=valoracion1.jugador.puesto, estado=True).values_list('cualidad__cualidad', flat=True)
        puesto2_cualidades = PuestoCualidad.objects.filter(puesto=valoracion2.jugador.puesto, estado=True).values_list('cualidad__cualidad', flat=True)

        # Unificar cualidades relevantes para ambos jugadores
        cualidades = list(set(puesto1_cualidades).union(set(puesto2_cualidades)))

        # Formatear datos de comparación
        data = {
            "cualidades": cualidades,
            "jugador1": {
                "nombre": f"{valoracion1.jugador.nombre} {valoracion1.jugador.apellido}",
                "valores": {cualidad: getattr(valoracion1, f"valoracion_{cualidad.lower()}", None) for cualidad in cualidades}
            },
            "jugador2": {
                "nombre": f"{valoracion2.jugador.nombre} {valoracion2.jugador.apellido}",
                "valores": {cualidad: getattr(valoracion2, f"valoracion_{cualidad.lower()}", None) for cualidad in cualidades}
            }
        }

        return JsonResponse(data)
    

from django.shortcuts import render

def handler404(request, exception):
    return render(request, '404.html', status=404)