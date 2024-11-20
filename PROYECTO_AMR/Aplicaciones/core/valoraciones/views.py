from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.db import transaction
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse_lazy
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.valoraciones.models import *
from Aplicaciones.paneladmin.submodulos.models import *
from Aplicaciones.core.valoraciones.forms import ValoracionForm, ValoracionDetalleForm


# Vista para el módulo principal de valoraciones
class ModuloValoracionesView(TemplateView):
    template_name = "modulo_valoraciones.html"


# Vista para el formulario de generar una nueva valoración
class CrearValoracionView(TemplateView):
    template_name = "valoracion_formulario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener jugadores activos
        jugadores = Jugador.objects.filter(estado=True)

        # Obtener la fecha y hora actual
        fecha_actual = now().date()
        hora_actual = now().time()

        # Pasar los jugadores y la fecha al contexto
        context.update({
            'jugadores': jugadores,
            'fecha_actual': fecha_actual,
            'hora_actual': hora_actual,
        })

        return context


# Cargar cualidades del jugador seleccionado
class CargarCualidadesView(View):
    def get(self, request, jugador_id):
        try:
            # Obtener el jugador seleccionado
            jugador = get_object_or_404(Jugador, id=jugador_id, estado=True)
            puesto = jugador.puesto  # Obtener el puesto del jugador

            # Verificar si el jugador tiene puesto y posición asociados
            puesto_nombre = puesto.abreviatura if puesto else "Sin puesto asignado"
            posicion_nombre = puesto.posicion.posicion if puesto and puesto.posicion else "Sin posición asignada"

            # Filtrar cualidades asociadas al puesto del jugador
            puesto_cualidades = PuestoCualidad.objects.filter(puesto=puesto, estado=True)

            # Preparar las cualidades y las estadísticas asociadas
            cualidades = []
            
            for pc in puesto_cualidades:
                estadisticas = Estadistica.objects.filter(cualidad=pc.cualidad, estado=True)
                cualidades.append({
                    "cualidad": pc.cualidad.cualidad,  # Nombre de la cualidad
                    "peso": float(pc.peso),  # Convertir peso a float para el frontend
                    "estadisticas": [{"id": est.id, "nombre": est.estadistica, "clave": est.estadistica.upper()} for est in estadisticas]
                })

            # Preparar respuesta JSON
            data = {
                "puesto": f"{puesto_nombre} - {posicion_nombre}",
                "cualidades": cualidades,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)


# Vista para guardar valoración y detalles
class GuardarValoracionView(FormView):
    template_name = 'valoracion_formulario.html'
    form_class = ValoracionForm
    success_url = reverse_lazy('valoraciones:modulo_valoraciones')  # Redirige al listado tras guardar

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Obtener jugador y descripción
                jugador_id = self.request.POST.get('jugador')
                jugador = get_object_or_404(Jugador, id=jugador_id)
                descripcion = self.request.POST.get('descripcion', '')

                # Crear cabecera de valoración
                valoracion = Valoracion.objects.create(
                    jugador=jugador,
                    descripcion=descripcion,
                    usuario_registro=self.request.user.username if self.request.user.is_authenticated else "Anónimo"
                )

                # Calcular y asignar valores a las cualidades
                cualidades = ['tiro', 'pase', 'velocidad', 'regate', 'defensa', 'fisico', 'reflejos', 'manejo', 'saque']
                for cualidad in cualidades:
                    promedio_cualidad = float(self.request.POST.get(f'calculo_{cualidad.upper()}', 0))
                    setattr(valoracion, f'valoracion_{cualidad}', promedio_cualidad)  # Asignar valor a cada campo

                # Inicializar variables
                suma_ponderada = 0
                total_cualidades = 0

                # Iterar sobre las cualidades y calcular los valores
                for cualidad in cualidades:
                    # Obtener el promedio de la cualidad desde el formulario
                    promedio_cualidad = float(self.request.POST.get(f'calculo_{cualidad.upper()}', 0))
                    # Obtener el peso de la cualidad para el jugador
                    peso_obj = PuestoCualidad.objects.filter(puesto=jugador.puesto, cualidad__cualidad=cualidad).first()
                    peso_valor = float(peso_obj.peso) if peso_obj else 0

                    # Verificar si el promedio o el peso son válidos antes de continuar
                    if promedio_cualidad > 0 and peso_valor > 0:
                        suma_ponderada += promedio_cualidad * peso_valor
                        total_cualidades += peso_valor  # Acumular el peso total

                    # Guardar el promedio en el campo correspondiente de la cabecera
                    setattr(valoracion, f'valoracion_{cualidad.lower()}', promedio_cualidad)

                # Obtener las cualidades asociadas al puesto del jugador
                puesto_cualidades = PuestoCualidad.objects.filter(puesto=jugador.puesto, estado=True)
                numero_cualidades = puesto_cualidades.count()  # Número real de cualidades asociadas

                # Calcular la valoración total dividiendo por el número real de cualidades asociadas al jugador
                valoracion.valoracion_total = (suma_ponderada / numero_cualidades) if numero_cualidades > 0 else 0
                valoracion.valoracion_total = min(valoracion.valoracion_total, 100)  # Limitar el máximo a 100

                # Guardar la cabecera
                valoracion.save()

                # Guardar detalles de estadísticas
                for key, value in self.request.POST.items():
                    if key.startswith('estadistica_'):
                        estadistica_nombre = key.split('_')[1]  # Extraer el nombre de la estadística
                        estadistica = get_object_or_404(Estadistica, estadistica=estadistica_nombre)
                        ValoracionDetalle.objects.create(
                            valoracion=valoracion,
                            estadistica=estadistica,
                            valor=float(value),
                            usuario_registro=self.request.user.username if self.request.user.is_authenticated else "Anónimo"
                        )

                messages.success(self.request, "Valoración guardada exitosamente.")
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f"Error al guardar la valoración: {e}")
            return redirect(self.success_url)


    def form_invalid(self, form):
        messages.error(self.request, "Formulario inválido. Verifique los datos ingresados.")
        return redirect(self.success_url)

