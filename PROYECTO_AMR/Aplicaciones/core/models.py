from django.db import models
from datetime import date
from Aplicaciones.paneladmin.submodulos.models import *
# Create your models here.

class Jugador(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    correo = models.EmailField(unique=True)
    puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT)
    fecha_nac = models.DateField()
    altura = models.IntegerField() #la altura del jugador en centimetros
    peso = models.DecimalField(max_digits=5, decimal_places=2) #el peso del jugador en kg, acepta maximo de 5 digitos entre ellos 2 decimales
    pierna_habil = models.CharField(max_length=10, choices=[('I', 'Izquierda'), ('D', 'Derecha'), ('A', 'Ambas')])
    foto = models.ImageField(upload_to='fotos/')
    estado = models.BooleanField(default=True)
    usuario = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def calcular_edad(self):
        """Calcula la edad del jugador a partir de su fecha de nacimiento."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nac.year
        if (hoy.month, hoy.day) < (self.fecha_nac.month, self.fecha_nac.day):
            edad -= 1
        return edad