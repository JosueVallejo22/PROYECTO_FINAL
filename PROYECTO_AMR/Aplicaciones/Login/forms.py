from django import forms

class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=50)
    clave = forms.CharField(widget=forms.PasswordInput)

##########

class NuevaClaveForm(forms.Form):
    nueva_clave = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese nueva contraseña'}),
        min_length=8,
        required=True,
        label="Nueva Contraseña"
    )
    confirmar_clave = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme nueva contraseña'}),
        min_length=8,
        required=True,
        label="Confirmar Contraseña"
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_clave = cleaned_data.get('nueva_clave')
        confirmar_clave = cleaned_data.get('confirmar_clave')

        # Validación para asegurarse de que las contraseñas coincidan
        if nueva_clave and confirmar_clave and nueva_clave != confirmar_clave:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Asegúrate de que la nueva contraseña cumpla con ciertos requisitos (opcional)
        # Puedes agregar más validaciones aquí si lo deseas, por ejemplo:
        # if not any(char.isdigit() for char in nueva_clave):
        #     raise forms.ValidationError("La contraseña debe contener al menos un número.")

        return cleaned_data

##################

### Formulario para cambiar contrasena
class CambioContrasenaForm(forms.Form):
    contrasena_actual = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña actual'}),
        required=True,
        label="Contraseña Actual"
    )
    nueva_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese nueva contraseña'}),
        min_length=8,
        required=True,
        label="Nueva Contraseña"
    )
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme nueva contraseña'}),
        min_length=8,
        required=True,
        label="Confirmar Contraseña"
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contrasena = cleaned_data.get('nueva_contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if nueva_contrasena and confirmar_contrasena and nueva_contrasena != confirmar_contrasena:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data