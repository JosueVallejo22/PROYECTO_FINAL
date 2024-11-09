from django.shortcuts import render, get_object_or_404, redirect
from Aplicaciones.paneladmin.submodulos.models import *
from Aplicaciones.Login.models import *
from Aplicaciones.paneladmin.submodulos.forms import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q



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

@method_decorator(admin_required, name='dispatch')
class MenuSubmodulos(View):
    
    def get(self, request):
        usuario_logueado = get_object_or_404(Usuario, id=request.session['user_id'])
        return render(request, 'menu_submodulos.html', {'usuario': usuario_logueado})

@method_decorator(admin_required, name='dispatch')
class PaisListView(ListView):
    model = Pais
    template_name = 'mantenimiento_paises.html'
    context_object_name = 'paises'
    queryset = Pais.objects.all().order_by('pais')
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Pais.objects.all().order_by('pais')
        if query:
            queryset = queryset.filter(
                Q(pais__icontains=query)
            )
        return queryset

@method_decorator(admin_required, name='dispatch')
class PaisCreateView(CreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'mantenimiento_paises.html'
    success_url = reverse_lazy('submodulos:mantenimiento_paises')

    def form_valid(self, form):
        messages.success(self.request, 'Pais registrado exitosamente.')
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paises'] = Pais.objects.all().order_by('pais')
        return context
    
@method_decorator(admin_required, name='dispatch')
class PaisUpdateView(UpdateView):
    model = Pais
    form_class = PaisForm
    template_name = 'mantenimiento_paises.html'
    success_url = reverse_lazy('submodulos:mantenimiento_paises')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paises'] = Pais.objects.all().order_by('pais')
        return context

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPais(View):
    def get(self, request, pk):
        pais = get_object_or_404(Pais, pk = pk)
        pais.estado = not pais.estado
        pais.save()
        messages.success(request, "Estado del pais actualizado exitosamente.")
        return redirect('submodulos:mantenimiento_paises')

###############################################################################################################
## MANTENIMIENTO CUALIDADES ##

@method_decorator(admin_required, name='dispatch')
class CualidadListView(ListView):
    model = Cualidad
    template_name = 'mantenimiento_cualidades.html'
    context_object_name = 'cualidades'
    queryset = Cualidad.objects.all().order_by('-estado','cualidad')
    paginate_by = 2

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
        return context


@method_decorator(admin_required, name='dispatch')
class CualidadCreateView(CreateView):
    model = Cualidad
    form_class = CualidadForm
    template_name = 'mantenimiento_cualidades.html'
    success_url = reverse_lazy('submodulos:mantenimiento_cualidades')

    def form_valid(self, form):
        messages.success(self.request, 'Cualidad creada exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cualidades'] = Cualidad.objects.all().order_by('cualidad')
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
        return context


@method_decorator(admin_required, name='dispatch')
class ActivarInactivarCualidad(View):
    def get(self, request, pk):
        cualidad = get_object_or_404(Cualidad, pk=pk)
        cualidad.estado = not cualidad.estado  # Invierte el valor de estado
        cualidad.save()
        messages.success(request, "Estado del rol actualizado exitosamente.")
        return redirect('submodulos:mantenimiento_cualidades')

###############################################################################################
### MANTENIMIENTO ESTADISTICAS ###
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
                Q(estadistica__icontains=search_query)  # Cambia 'nombre' al campo adecuado en el modelo Estadistica
            )

        if cualidad_filter:
            queryset = queryset.filter(cualidad__id=cualidad_filter)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EstadisticaForm()
        context['cualidades'] = Cualidad.objects.all().order_by('cualidad')  # Para el select de cualidades
        context['search'] = self.request.GET.get('search', '')
        context['cualidad_selected'] = self.request.GET.get('cualidad', '')
        return context


@method_decorator(admin_required, name='dispatch')
class EstadisticasCreateView(CreateView):
    model = Estadistica
    form_class = EstadisticaForm
    template_name = 'mantenimiento_estadisticas.html'
    success_url = reverse_lazy('submodulos:mantenimiento_estadisticas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estadisticas'] = Estadistica.objects.all().order_by('cualidad')
        return context
    
@method_decorator(admin_required, name='dispatch')
class EstadisticaUpdateView(UpdateView):
    model = Estadistica
    form_class = EstadisticaForm
    template_name = 'mantenimiento_estadisticas.html'
    success_url = reverse_lazy('submodulos:mantenimiento_estadisticas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estadisticas'] = Estadistica.objects.all().order_by('cualidad')
        return context

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarEstadistica(View):
    def get(self, request, pk):
        estadistica = get_object_or_404(Estadistica, pk=pk)
        estadistica.estado = not estadistica.estado
        estadistica.save()
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
        return context


@method_decorator(admin_required, name='dispatch')
class PosicionCreateView(CreateView):
    model = Posicion
    form_class = PosicionForm
    template_name = 'mantenimiento_posicion.html'
    success_url = reverse_lazy('submodulos:mantenimiento_posicion')

    def form_valid(self, form):
        messages.success(self.request, 'Posicion registrada exitosamente.')
        return super().form_valid(form)
    

@method_decorator(admin_required, name='dispatch')
class PosicionUpdateView(UpdateView):
    model = Posicion
    form_class = PosicionForm
    template_name = 'mantenimiento_posicion.html'
    success_url = reverse_lazy('submodulos:mantenimiento_posicion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posiciones'] = Posicion.objects.all()
        return context

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPosicion(View):
    def get(self, request, pk):
        posicion = get_object_or_404(Posicion, pk = pk)
        posicion.estado = not posicion.estado
        posicion.save()
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
    
@method_decorator(admin_required, name='dispatch')
class PuestoUpdateView(UpdateView):
    model = Puesto
    form_class = PuestoForm
    template_name = 'mantenimiento_puesto.html'
    success_url = reverse_lazy('submodulos:mantenimiento_puesto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puestos'] = Puesto.objects.all().order_by('posicion')
        return context
    
@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPuesto(View):
    def get(self, request, pk):
        puesto = get_object_or_404(Puesto, pk=pk)
        puesto.estado = not puesto.estado
        puesto.save()
        messages.success
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
        return context

@method_decorator(admin_required, name='dispatch')
class PuestoCualidadCreateView(CreateView):
    model = PuestoCualidad
    form_class = PuestoCualidadForm
    template_name = 'cualidad_puesto.html'
    success_url = reverse_lazy('submodulos:mantenimiento_puesto_cualidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puestos_cualidades'] = PuestoCualidad.objects.all().order_by('puesto', 'cualidad')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Puesto-Cualidad creado exitosamente.')
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class PuestoCualidadUpdateView(UpdateView):
    model = PuestoCualidad
    form_class = PuestoCualidadForm
    template_name = 'cualidad_puesto.html'
    success_url = reverse_lazy('submodulos:mantenimiento_puesto_cualidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puestos_cualidades'] = PuestoCualidad.objects.all().order_by('puesto', 'cualidad')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Puesto-Cualidad actualizado exitosamente.')
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class ActivarInactivarPuestoCualidad(View):
    def get(self, request, pk):
        puesto_cualidad = get_object_or_404(PuestoCualidad, pk=pk)
        puesto_cualidad.estado = not puesto_cualidad.estado
        puesto_cualidad.save()
        return redirect('submodulos:mantenimiento_puesto_cualidad')