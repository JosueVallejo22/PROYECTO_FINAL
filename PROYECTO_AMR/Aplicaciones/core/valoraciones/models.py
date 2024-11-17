from django.db import models
from Aplicaciones.core.models import *
from Aplicaciones.Login.models import *
from Aplicaciones.paneladmin.submodulos.models import Estadistica
# Create your models here.

#valoracion cabecera 
class Valoracion(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=128, null=True, blank=True)
    
    # Campos de evaluación
    valoracion_total = models.FloatField(null=True, blank=True)
    valoracion_tiro = models.FloatField(null=True, blank=True)
    valoracion_pase = models.FloatField(null=True, blank=True)
    valoracion_velocidad = models.FloatField(null=True, blank=True)
    valoracion_regate = models.FloatField(null=True, blank=True)
    valoracion_defensa = models.FloatField(null=True, blank=True)
    valoracion_fisico = models.FloatField(null=True, blank=True)
    valoracion_reflejos = models.FloatField(null=True, blank=True)
    valoracion_manejo = models.FloatField(null=True, blank=True)
    valoracion_saque = models.FloatField(null=True, blank=True)

    # Campos de auditoría
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    hora_registro = models.TimeField(auto_now_add=True)
    hora_actualizacion = models.TimeField(auto_now=True)
    usuario_registro = models.CharField(max_length=50, null=True, blank=True)
    usuario_modificacion = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"Valoración de {self.jugador} - {self.fecha_registro}"
    
    class Meta:
        verbose_name = 'Valoracion Cabecera'
        verbose_name_plural = 'Valoraciones Cabeceras'
        ordering = ['-fecha_registro']

#Valoracion detalles
class ValoracionDetalle(models.Model):
    valoracion = models.ForeignKey(Valoracion, on_delete=models.PROTECT, related_name='detalles')
    estadistica = models.ForeignKey(Estadistica, on_delete=models.PROTECT)
    valor = models.FloatField()
    
    # Campos de auditoría
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    usuario_registro = models.CharField(max_length=50, null=True, blank=True)
    usuario_modificacion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Detalle de {self.valoracion} - {self.estadistica} : {self.valor}"

    class Meta:
        verbose_name = 'Detalle de Valoración'
        verbose_name_plural = 'Detalles de Valoración'