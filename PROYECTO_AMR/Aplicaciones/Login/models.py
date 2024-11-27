from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import random
import string
from django.core.validators import RegexValidator



class Rol(models.Model):
    rol = models.CharField(max_length=50, unique=True)
    estado = models.BooleanField(default=True)  # Estado Activo por defecto

    def save(self, *args, **kwargs):
        # Convierte los roles a mayúsculas
        self.rol = self.rol.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.rol

    class Meta:
        verbose_name_plural = "Roles"



class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    numero_telefono = models.CharField(
            max_length=10,
            unique=True,
            validators=[
                RegexValidator(
                    regex=r'^(?:09\d{8}|0[2-7]\d{7})$',
                    message="Ingrese un número de teléfono ecuatoriano válido (móvil o fijo)."
                )
            ],
            help_text="Ejemplo: 0991234567 para móvil o 022345678 para fijo."
        )    
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    clave = models.CharField(max_length=128 )    
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_used = models.BooleanField(default=False)
    ultimo_inicio_sesion = models.DateTimeField(null=True, blank=True)
    cambio_pass = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.clave and not self.clave.startswith('pbkdf2_sha256$'):
            self.clave = make_password(self.clave)
        super().save(*args, **kwargs)


    def check_password(self, raw_password):
        return check_password(raw_password, self.clave)
    
    def get_sexo_display(self):
        if self.sexo == 'M':
            return 'Masculino'
        elif self.sexo == 'F':
            return 'Femenino'
        return 'No definido'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.nombre_usuario} - {self.rol}"

    class Meta:
        verbose_name_plural = "Usuarios"

    def generar_contrasena_temporal(self, length=8):
        # Genera una contraseña aleatoria de letras y dígitos.
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(length))