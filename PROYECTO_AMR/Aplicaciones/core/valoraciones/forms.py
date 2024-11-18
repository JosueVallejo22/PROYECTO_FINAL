from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from Aplicaciones.core.models import *
from Aplicaciones.core.valoraciones.models import *
from Aplicaciones.paneladmin.submodulos.models import *
from django import forms


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
