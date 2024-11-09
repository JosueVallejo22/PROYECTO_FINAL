from django.db import models

# Create your models here.
class Pais(models.Model):
    pais = models.CharField(max_length=30)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pais
    
    class Meta:
        verbose_name_plural = "Paises"


class Cualidad(models.Model):
    cualidad = models.CharField(max_length=64)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cualidad
    
    class Meta:
        verbose_name_plural = "Tipo de Cualidades"

class Estadistica(models.Model):
    estadistica = models.CharField(max_length=64)
    cualidad = models.ForeignKey(Cualidad, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.estadistica
    
    class Meta:
        verbose_name_plural = "Estadisticas"


class Posicion(models.Model):
    posicion = models.CharField(max_length=10, unique=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.posicion
    
    class Meta:
        verbose_name_plural = "Posiciones"

class Puesto(models.Model):
    puesto = models.CharField(max_length=30, unique=True)
    abreviatura = models.CharField(max_length=5, unique=True)
    posicion = models.ForeignKey(Posicion, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.puesto
    
    class Meta:
        verbose_name_plural = "Puestos"


class PuestoCualidad(models.Model):
    puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT)
    cualidad = models.ForeignKey(Cualidad, on_delete=models.PROTECT)
    peso = models.DecimalField(max_digits=2, decimal_places=1)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.puesto} {self.estadistica} - {self.estado}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['puesto', 'cualidad'], name='unique_puesto_cualidad')
        ]
        verbose_name_plural = "Puestos - Estadisticas"

    