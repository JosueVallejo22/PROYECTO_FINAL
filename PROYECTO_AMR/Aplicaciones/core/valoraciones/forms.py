from django import forms
from Aplicaciones.core.models import Jugador
from Aplicaciones.core.valoraciones.models import Valoracion, ValoracionDetalle
from Aplicaciones.paneladmin.submodulos.models import Estadistica
from django.utils.timezone import now


class SeleccionJugadorForm(forms.Form):
    jugador = forms.ModelChoiceField(
        queryset=Jugador.objects.filter(estado=True),
        label="Seleccionar Jugador",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )


class EstadisticasValoracionForm(forms.Form):
    def __init__(self, *args, estadisticas=None, **kwargs):
        super().__init__(*args, **kwargs)
        if estadisticas:
            for estadistica in estadisticas:
                self.fields[f"estadistica_{estadistica.id}"] = forms.FloatField(
                    label=estadistica.estadistica,
                    required=False,
                    widget=forms.NumberInput(attrs={"class": "form-control"}),
                )


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['jugador', 'descripcion', 'valoracion_tiro', 'valoracion_pase', 'valoracion_velocidad',
                  'valoracion_regate', 'valoracion_defensa', 'valoracion_fisico', 'valoracion_reflejos',
                  'valoracion_manejo', 'valoracion_saque']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
        }

    def save(self, commit=True):
        # Asignar la fecha y hora actual a la valoración
        self.instance.fecha_registro = now().date()
        self.instance.hora_registro = now().time()
        return super().save(commit)


class ValoracionDetalleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        estadisticas = kwargs.pop('estadisticas', None)
        super().__init__(*args, **kwargs)
        if estadisticas:
            for estadistica in estadisticas:
                self.fields[f"estadistica_{estadistica.id}"] = forms.FloatField(
                    label=estadistica.estadistica,
                    required=False,
                    widget=forms.NumberInput(attrs={"class": "form-control"}),
                )
