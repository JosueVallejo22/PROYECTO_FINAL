from django import forms
from Aplicaciones.Login.models import *


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['rol']
        widgets = {
            'rol': forms.TextInput(attrs={'class':'form-control', 'placeholder':'INGRESE EL ROL'})
        }
        labels = {
            'rol':'ROL',
        }
    
    def clean_rol(self):
        rol = self.cleaned_data['rol'].upper()  # Asegúrate de convertir a mayúsculas aquí
        if Rol.objects.filter(rol=rol).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('EL ROL INGRESADO YA EXISTE.')
        return rol

from django.forms.widgets import DateInput

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellido',
            'nombre_usuario',
            'correo',
            'numero_telefono',
            'fecha_nacimiento',
            'sexo',
            'rol',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese apellido'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre de usuario'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese correo electrónico'}),
            'numero_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese número de teléfono', 'maxlength': '15'}),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 
                'text', 
                'placeholder': 'Seleccione la fecha',
                'id': 
                'id_fecha_nacimiento'}
            ),

            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'nombre_usuario': 'Nombre de Usuario',
            'correo': 'Correo Electrónico',
            'numero_telefono': 'Número de Teléfono',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'sexo': 'Sexo',
            'rol': 'Rol',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.filter(estado=True)

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Usuario.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("El correo ingresado ya se encuentra registrado.")
        return correo

    def clean_numero_telefono(self):
        numero = self.cleaned_data.get('numero_telefono')
        if not numero.isdigit():
            raise forms.ValidationError("El número de teléfono solo debe contener dígitos.")
        if Usuario.objects.filter(numero_telefono=numero).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un Usuario con este número de teléfono.")
        return numero
