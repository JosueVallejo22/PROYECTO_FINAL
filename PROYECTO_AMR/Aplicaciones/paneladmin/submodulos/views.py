from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Aplicaciones.paneladmin.submodulos.models import *
from Aplicaciones.Login.models import *
from Aplicaciones.paneladmin.submodulos.forms import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from Aplicaciones.Auditoria.utils import save_audit
from Aplicaciones.core.models import Jugador
from Aplicaciones.Auditoria.models import *



# Create your views here.
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

##

@method_decorator(admin_required, name='dispatch')
class MenuSubmodulos(View):
    
    def get(self, request):
        usuario_logueado = get_object_or_404(Usuario, id=request.session['user_id'])
        return render(request, 'menu_submodulos.html', {'usuario': usuario_logueado})

##

@method_decorator(admin_required, name='dispatch')
class PaisListView(ListView):
    model = Pais
    template_name = 'mantenimiento_paises.html'
    context_object_name = 'paises'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Pais.objects.all().order_by('pais')
        if query:
            queryset = queryset.filter(Q(pais__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clear_url'] = self.request.path
        return context


@method_decorator(admin_required, name='dispatch')
class PaisCreateView(CreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'mantenimiento_paises.html'
    success_url = reverse_lazy('submodulos:mantenimiento_paises')

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, 'País registrado exitosamente.')
        return response

    def form_invalid(self, form):
        # Si el formulario es inválido, redirige a la lista y muestra errores.
        messages.error(self.request, 'Error al registrar el país. Verifique los datos ingresados.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paises'] = Pais.objects.all().order_by('pais')
        context['clear_url'] = self.request.path
        return context


@method_decorator(admin_required, name='dispatch')
class PaisUpdateView(UpdateView):
    model = Pais
    form_class = PaisForm
    template_name = 'mantenimiento_paises.html'
    success_url = reverse_lazy('submodulos:mantenimiento_paises')

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'País modificado exitosamente.')
        return response

    def form_invalid(self, form):
        # Si el formulario es inválido, redirige a la lista y muestra errores.
        messages.error(self.request, 'Error al modificar el país. Verifique los datos ingresados.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paises'] = Pais.objects.all().order_by('pais')
        context['clear_url'] = self.request.path
        return context


@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPais(View):
    def get(self, request, pk):
        pais = get_object_or_404(Pais, pk=pk)
        pais.estado = not pais.estado
        pais.save()
        save_audit(self.request, pais, action='M')
        estado = "activado" if pais.estado else "inactivado"
        messages.success(request, f"Estado del país actualizado exitosamente. El país ha sido {estado}.")
        return redirect('submodulos:mantenimiento_paises')

from django.http import JsonResponse

def api_paises(request):
    query = request.GET.get('q', '')
    if query:
        paises = Pais.objects.filter(pais__icontains=query).values('pais')
    else:
        paises = Pais.objects.all().values('pais')
    return JsonResponse(list(paises), safe=False)

###############################################################################################################
## MANTENIMIENTO CUALIDADES ##

@method_decorator(admin_required, name='dispatch')
class CualidadListView(ListView):
    model = Cualidad
    template_name = 'mantenimiento_cualidades.html'
    context_object_name = 'cualidades'
    queryset = Cualidad.objects.all().order_by('-estado','cualidad')
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Cualidad.objects.all().order_by('-estado', 'cualidad')
        if query:
            queryset = queryset.filter(
                Q(cualidad__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  # Pasar la búsqueda al contexto para mantenerla en la vista
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context


@method_decorator(admin_required, name='dispatch')
class CualidadCreateView(CreateView):
    model = Cualidad
    form_class = CualidadForm
    template_name = 'mantenimiento_cualidades.html'
    success_url = reverse_lazy('submodulos:mantenimiento_cualidades')

    def form_valid(self, form):
        response =  super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, 'Cualidad creada exitosamente.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cualidades'] = Cualidad.objects.all().order_by('cualidad')
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context

@method_decorator(admin_required, name='dispatch')
class CualidadUpdateView(UpdateView):
    model = Cualidad
    form_class = CualidadForm
    template_name = 'mantenimiento_cualidades.html'
    success_url = reverse_lazy('submodulos:mantenimiento_cualidades')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cualidades'] = Cualidad.objects.all().order_by('cualidad')
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context
    
    def form_valid(self, form):
        response =  super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'Cualidad modificada exitosamente.')
        return response


@method_decorator(admin_required, name='dispatch')
class ActivarInactivarCualidad(View):
    def get(self, request, pk):
        cualidad = get_object_or_404(Cualidad, pk=pk)
        cualidad.estado = not cualidad.estado  # Invierte el valor de estado
        cualidad.save()
        save_audit(self.request, cualidad, action='M')
        messages.success(request, "Estado de la cualidad actualizado exitosamente.")
        return redirect('submodulos:mantenimiento_cualidades')

###############################################################################################
### MANTENIMIENTO ESTADISTICAS ###
from django.db.models import Q
from django.shortcuts import get_object_or_404

@method_decorator(admin_required, name='dispatch')
class EstadisticasListView(ListView):
    model = Estadistica
    template_name = 'mantenimiento_estadisticas.html'
    context_object_name = 'estadisticas'
    queryset = Estadistica.objects.all().order_by('cualidad')
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        cualidad_filter = self.request.GET.get('cualidad', '')

        if search_query:
            queryset = queryset.filter(
                Q(estadistica__icontains=search_query)
            )

        if cualidad_filter:
            queryset = queryset.filter(cualidad__id=cualidad_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EstadisticaForm()  # Formulario actualizado
        context['search'] = self.request.GET.get('search', '')
        context['cualidades'] = Cualidad.objects.all().order_by('id')  # Opciones del filtro
        context['cualidad_selected'] = self.request.GET.get('cualidad', '')  # Mantener seleccionada la opción
        context['clear_url'] = self.request.path  # URL para limpiar filtros
        return context


@method_decorator(admin_required, name='dispatch')
class EstadisticasCreateView(CreateView):
    model = Estadistica
    form_class = EstadisticaForm
    template_name = 'mantenimiento_estadisticas.html'
    success_url = reverse_lazy('submodulos:mantenimiento_estadisticas')

    def form_valid(self, form):
        # No necesitas manejar `cualidad` aquí, ya que se asigna automáticamente en el modelo.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estadisticas'] = Estadistica.objects.all().order_by('cualidad')
        context['form'] = self.get_form()
        context['cualidades'] = Cualidad.objects.all().order_by('id')  # Select de cualidades
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context


@method_decorator(admin_required, name='dispatch')
class EstadisticaUpdateView(UpdateView):
    model = Estadistica
    form_class = EstadisticaForm
    template_name = 'mantenimiento_estadisticas.html'
    success_url = reverse_lazy('submodulos:mantenimiento_estadisticas')

    def form_valid(self, form):
        # La asignación automática de `cualidad` ya está manejada en el modelo.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estadisticas'] = Estadistica.objects.all().order_by('cualidad')
        context['form'] = self.get_form()
        context['cualidades'] = Cualidad.objects.all().order_by('id')  # Select de cualidades
        return context

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarEstadistica(View):
    def get(self, request, pk):
        estadistica = get_object_or_404(Estadistica, pk=pk)
        estadistica.estado = not estadistica.estado
        estadistica.save()
        save_audit(request, estadistica, action='M')
        messages.success(request, "Estado de la Estadística actualizado exitosamente.")
        return redirect('submodulos:mantenimiento_estadisticas')


###################################################################
# MANTENIMIENTO POSICION

@method_decorator(admin_required, name='dispatch')
class PosicionListView(ListView):
    model = Posicion
    template_name = 'mantenimiento_posicion.html'
    context_object_name = 'posiciones'
    queryset = Posicion.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PosicionForm()
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context


@method_decorator(admin_required, name='dispatch')
class PosicionCreateView(CreateView):
    model = Posicion
    form_class = PosicionForm
    template_name = 'mantenimiento_posicion.html'
    success_url = reverse_lazy('submodulos:mantenimiento_posicion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posiciones'] = Posicion.objects.all()
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context
    

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, 'Posicion registrada exitosamente.')
        return response
    

@method_decorator(admin_required, name='dispatch')
class PosicionUpdateView(UpdateView):
    model = Posicion
    form_class = PosicionForm
    template_name = 'mantenimiento_posicion.html'
    success_url = reverse_lazy('submodulos:mantenimiento_posicion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posiciones'] = Posicion.objects.all()
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'Posicion modificada exitosamente.')
        return response

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPosicion(View):
    def get(self, request, pk):
        posicion = get_object_or_404(Posicion, pk = pk)
        posicion.estado = not posicion.estado
        posicion.save()
        save_audit(self.request, posicion, action='M')
        messages.success(self.request, 'Estado de la Posicion actualizado exitosamente.')
        return redirect('submodulos:mantenimiento_posicion')

###############################################################################
### MANTENIMIENTO PUESTOS
@method_decorator(admin_required, name='dispatch')
class PuestoListView(ListView):
    model = Puesto
    template_name = 'mantenimiento_puesto.html'
    context_object_name = 'puestos'
    queryset = Puesto.objects.all().order_by('posicion')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PuestoForm()
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context


@method_decorator(admin_required, name='dispatch')
class PuestoCreateView(CreateView):
    model = Puesto
    form_class = PuestoForm
    template_name = 'mantenimiento_puesto.html'
    success_url = reverse_lazy('submodulos:mantenimiento_puesto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puestos'] = Puesto.objects.all().order_by('posicion')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, 'Puesto registrado exitosamente.')
        return response
    
@method_decorator(admin_required, name='dispatch')
class PuestoUpdateView(UpdateView):
    model = Puesto
    form_class = PuestoForm
    template_name = 'mantenimiento_puesto.html'
    success_url = reverse_lazy('submodulos:mantenimiento_puesto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puestos'] = Puesto.objects.all().order_by('posicion')
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'Puesto modificado exitosamente.')
        return response
    
@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPuesto(View):
    def get(self, request, pk):
        puesto = get_object_or_404(Puesto, pk=pk)
        puesto.estado = not puesto.estado
        puesto.save()
        save_audit(self.request, puesto, action='M')
        messages.success(self.request, 'Estado del puesto actualizado exitosamente.')
        return redirect('submodulos:mantenimiento_puesto')


##########################################################################
#

@method_decorator(admin_required, name='dispatch')
class PuestoCualidadListView(ListView):
    model = PuestoCualidad
    template_name = 'cualidad_puesto.html'
    context_object_name = 'puestos_cualidades'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        puesto_filter = self.request.GET.get('puesto', '')

        if search_query:
            queryset = queryset.filter(
                Q(cualidad__cualidad__icontains=search_query) |
                Q(puesto__puesto__icontains=search_query)
            )

        if puesto_filter:
            queryset = queryset.filter(puesto__id=puesto_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PuestoCualidadForm()
        context['puestos'] = Puesto.objects.filter(estado=True).order_by('puesto')
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context

@method_decorator(admin_required, name='dispatch')
class PuestoCualidadCreateView(CreateView):
    model = PuestoCualidad
    form_class = PuestoCualidadForm
    template_name = 'cualidad_puesto.html'
    success_url = reverse_lazy('submodulos:mantenimiento_puesto_cualidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        context['puestos_cualidades'] = PuestoCualidad.objects.all().order_by('puesto', 'cualidad')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='A')
        messages.success(self.request, 'Puesto-Cualidad creado exitosamente.')
        return response

@method_decorator(admin_required, name='dispatch')
class PuestoCualidadUpdateView(UpdateView):
    model = PuestoCualidad
    form_class = PuestoCualidadForm
    template_name = 'cualidad_puesto.html'
    success_url = reverse_lazy('submodulos:mantenimiento_puesto_cualidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puestos_cualidades'] = PuestoCualidad.objects.all().order_by('puesto', 'cualidad')
        context['clear_url'] = self.request.path  # Define la URL para el botón "Limpiar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        save_audit(self.request, self.object, action='M')
        messages.success(self.request, 'Puesto-Cualidad modificado exitosamente.')
        return response
    
@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPuestoCualidad(View):
    def get(self, request, pk):
        puesto_cualidad = get_object_or_404(PuestoCualidad, pk=pk)
        puesto_cualidad.estado = not puesto_cualidad.estado
        puesto_cualidad.save()
        save_audit(self.request, puesto_cualidad, action='M')
        messages.success(self.request, 'Estado del Puesto-Cualidad actualizado exitosamente.')
        return redirect('submodulos:mantenimiento_puesto_cualidad')



###### 
@method_decorator(admin_required, name='dispatch')
class ListarJugador(ListView):
    model = Jugador
    template_name = 'lista_jugadores_admin.html'
    context_object_name = 'listjugadores'
    paginate_by = 5  # Si deseas paginación

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()  # Búsqueda
        puesto_filter = self.request.GET.get('puesto', '')  # Filtro por puesto

        # Filtra jugadores activos y ordenados por nombre
        queryset = Jugador.objects.filter(estado=False).order_by('nombre')

        if query:
            # Filtra por nombre o apellido
            queryset = queryset.filter(
                Q(nombre__icontains=query) | Q(apellido__icontains=query)
            )

        if puesto_filter:
            # Filtra por puesto (relación FK)
            queryset = queryset.filter(puesto_id=puesto_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puestos'] = Puesto.objects.all().order_by('puesto')  # Opciones para el filtro de puesto
        context['puesto_selected'] = self.request.GET.get('puesto', '')  # Opción seleccionada
        context['search'] = self.request.GET.get('q', '')  # Valor del campo de búsqueda
        context['clear_url'] = self.request.path  # URL para el botón "Limpiar"
        return context



@method_decorator(admin_required, name='dispatch')
class DetalleJugadores(DetailView):
    """Vista para mostrar detalles de un jugador"""
    model = Jugador
    template_name = 'det_jugadores_admin.html'
    context_object_name = 'detjugadores'

@method_decorator(admin_required, name='dispatch')
class JugadorCreateView(CreateView):
    """vista para crear un nuevo jugador"""
    template_name = 'form_jugador_admin.html'
    model = Jugador
    form_class = JugadorADForm
    success_url = reverse_lazy('submodulos:listar_jugador_admin')

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

@method_decorator(admin_required, name='dispatch')
class JugadorUpdateView(UpdateView):
    """Vista para actualizar un jugador existente"""
    template_name = 'form_jugador_admin.html'
    model = Jugador
    form_class = JugadorADForm
    success_url = reverse_lazy('submodulos:listar_jugador_admin')


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

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarJugadorAd(View):
    """Vista para activar/inactivar un rol"""
    def get(self, request, pk):
        jugador = get_object_or_404(Jugador, pk=pk)
        jugador.estado = not jugador.estado
        
        user_id = self.request.session.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        jugador.usuario = usuario.nombre_usuario

        jugador.save()
        save_audit(self.request, jugador, action='M')
        messages.success(request, "Estado del jugador actualizado exitosamente.")
        return redirect('submodulos:listar_jugador_admin')
    
###########################################################################################################################################

@method_decorator(admin_required, name='dispatch')
class ListaCambios(ListView):
    """Vista para listar registros de auditoría con filtros y búsqueda"""
    model = AuditoriaUsuario
    template_name = 'historial_cambios.html'
    context_object_name = 'auditoria'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha', '-hora')
        search_query = self.request.GET.get('search', '')
        usuario_filter = self.request.GET.get('usuario', '')
        accion_filter = self.request.GET.get('accion', '')

        if search_query:
            queryset = queryset.filter(
                Q(usuario__nombre_usuario__icontains=search_query) |
                Q(tabla__icontains=search_query)
            )

        if usuario_filter:
            queryset = queryset.filter(usuario__id=usuario_filter)
        
        if accion_filter:
            queryset = queryset.filter(accion=accion_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener opciones del campo `tipo_accion` (choices)
        acciones = AuditoriaUsuario.tipo_accion  # Esto devuelve [('A', 'A'), ('M', 'M'), ('E', 'E')]

        # Mapear códigos de acción a nombres legibles
        context['acciones'] = [{"codigo": accion[0], "nombre": "Adición" if accion[0] == "A" else "Modificación" if accion[0] == "M" else "Eliminación"} for accion in acciones]

        context['usuarios'] = Usuario.objects.all().order_by('nombre_usuario')  # Opciones para el filtro de usuario
        context['usuario_selected'] = self.request.GET.get('usuario', '')  # Usuario seleccionado
        context['accion_selected'] = self.request.GET.get('accion', '')  # Acción seleccionada
        context['search'] = self.request.GET.get('search', '')  # Valor del campo de búsqueda
        context['clear_url'] = self.request.path  # URL para limpiar filtros

        detalle_id = self.request.GET.get('detalle')
        if detalle_id:
            context['detalle_auditoria'] = get_object_or_404(AuditoriaUsuario, pk=detalle_id)
        
        return context

