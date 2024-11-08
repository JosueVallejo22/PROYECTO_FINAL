from django import forms
from django.forms import ModelForm
from Aplicaciones.core.models import Jugador

class JugadorForm(ModelForm):
    class Meta:
        model = Jugador
        fields = [
            'nombre',
            'apellido',
            'pais',
            'correo',
            'puesto',
            'fecha_nac',
            'altura',
            'peso',
            'pierna_habil',
            'foto',
        ]
        widgets = {
        'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese el nombre', 'required': False}),
        'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el apellido', 'required': False}),
        'pais': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Pais', 'required': False}),
        'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese correo'}),
        'fecha_nac': forms.DateInput(attrs={ 'class': 'form-control','placeholder': 'Ingrese la fecha (YYYY-MM-DD)', 'required': False, 'type': 'date'}),
        'puesto': forms.Select(attrs={'class': 'form-control', 'placeholder': '', 'required': False}),
        'pierna_habil': forms.Select(attrs={'class': 'form-control', 'placeholder': '', 'required': False}),
        'peso': forms.NumberInput(attrs={'class': 'form-control', 'required': False}),
        'altura': forms.NumberInput(attrs={'class': 'form-control', 'required': False}),
        'foto': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
        }
        labels = {
            'nombre':'Nombre',
            'apellido':'Apellido',
            'pais':'Nacionalidad',
            'correo':'Correo',
            'fecha_nac':'Fecha de Nacimiento',
            'puesto':'Puesto',
            'pierna_habil':'Pierna Habil',
            'altura':'Altura',
            'peso':'Peso',
            'imagen':'Foto',
        }