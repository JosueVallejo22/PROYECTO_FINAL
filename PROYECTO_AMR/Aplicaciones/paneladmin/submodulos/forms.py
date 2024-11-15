from django import forms
from Aplicaciones.paneladmin.submodulos.models import *
from Aplicaciones.core.models import Jugador


class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['pais']
        widgets = {
            'pais': forms.TextInput(attrs={'class':'form-control', 'placeholder':'INGRESE EL PAIS'})
        }
        labels = {
            'pais':'PAIS',
        }
    
    def clean_pais(self):
        pais = self.cleaned_data['pais'].upper()  # Asegúrate de convertir a mayúsculas aquí
        if Pais.objects.filter(pais=pais).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('EL PAIS INGRESADO YA EXISTE.')
        return pais
#####

class CualidadForm(forms.ModelForm):
    class Meta:
        model = Cualidad
        fields = ['cualidad']
        widgets = {
            'cualidad': forms.TextInput(attrs={'class':'form-control', 'placeholder':'INGRESE LA CUALIDAD'})
        }
        labels = {
            'cualidad':'CUALIDAD'
        }
    def clean_cualidad(self):
        cualidad = self.cleaned_data['cualidad'].upper()
        if Cualidad.objects.filter(cualidad=cualidad).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('LA CUALIDAD INGRESADA YA EXISTE.')
        return cualidad
    
###
class EstadisticaForm(forms.ModelForm):
    class Meta:
        model = Estadistica
        fields = [
            'estadistica',
            'cualidad',
        ]
        widgets = {
            'estadistica': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el nombre de la estadistica.'}),
            'cualidad': forms.Select(attrs={'class':'form-control'}),
        }

        labels = {
            'estadistica': 'ESTADISTICA',
            'cualidad': 'CUALIDAD'
        }

    def __init__(self, *args, **kwargs):
        super(EstadisticaForm, self).__init__(*args, **kwargs)
        self.fields['cualidad'].queryset = Cualidad.objects.filter(estado=True)

        
    def clean_estadistica(self):
        estadistica = self.cleaned_data['estadistica'].upper()
        if self.instance and Estadistica.objects.filter(estadistica=estadistica).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('LA ESTADISTICA INGRESADA YA EXISTE.')
        return estadistica


######
#MANTENIMIENTO POSICION

class PosicionForm(forms.ModelForm):
    class Meta:
        model = Posicion
        fields = ['posicion']
        widgets = {
            'posicion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'INGRESE LA POSICION'})
        }

        labels = {
            'posicion':'POSICION',
        }
    
    def clean_posicion(self):
        posicion = self.cleaned_data['posicion'].upper()
        if Posicion.objects.filter(posicion = posicion).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('LA POSICION INGRESADA YA EXISTE.')
        return posicion


#########
### MANTENIMIENTO PUESTOS

class PuestoForm(forms.ModelForm):
    class Meta:
        model = Puesto
        fields = ['puesto', 'abreviatura', 'posicion']
        widgets = {
            'puesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INGRESE EL PUESTO'}),
            'abreviatura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INGRESE LA ABREVIATURA'}),
            'posicion': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'puesto': 'PUESTO',
            'abreviatura': 'ABREVIATURA',
            'posicion': 'POSICION',
        }

    def __init__(self, *args, **kwargs):
        super(PuestoForm, self).__init__(*args, **kwargs)
        self.fields['posicion'].queryset = Posicion.objects.filter(estado=True)

    def clean_puesto(self):
        puesto = self.cleaned_data['puesto'].upper()
        if self.instance and Puesto.objects.filter(puesto=puesto).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('EL PUESTO INGRESADO YA EXISTE.')
        return puesto

    def clean_abreviatura(self):
        abreviatura = self.cleaned_data['abreviatura'].upper()
        if self.instance and Puesto.objects.filter(abreviatura=abreviatura).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('LA ABREVIATURA INGRESADA YA EXISTE.')
        return abreviatura

######
# CUALIDAD - PUESTO

class PuestoCualidadForm(forms.ModelForm):
    class Meta:
        model = PuestoCualidad
        fields = ['puesto', 'cualidad', 'peso',]
        widgets = {
            'puesto': forms.Select(attrs={'class': 'form-control'}),
            'cualidad': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el peso de la cualidad conforme el puesto (1.1 - 2.0)'}),
        }
        labels = {
            'puesto': 'Puesto',
            'cualidad': 'Cualidad',
            'peso': 'Peso (%)',
        }

    def clean_peso(self):
        peso = self.cleaned_data['peso']
        if peso < 1 or peso > 2:
            raise forms.ValidationError('El peso debe estar entre 1 y 2.')
        return peso

#################################
class JugadorADForm(forms.ModelForm):
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