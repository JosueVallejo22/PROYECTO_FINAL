from django.db import models
from Aplicaciones.Login.models import Usuario
# Create your models here.

class AuditoriaUsuario(models.Model):
    tipo_accion = (
        ('A','A'), #Adicion
        ('M','M'), #Modificar
        ('E','E'), #Eliminar
    )
    usuario = models.ForeignKey(Usuario, verbose_name='Usuario', on_delete=models.PROTECT)
    tabla = models.CharField(max_length=100, verbose_name='Tabla')
    registroid = models.IntegerField(verbose_name='Registro ID')
    accion = models.CharField(choices=tipo_accion, max_length=10, verbose_name='Accion')
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')
    estacion = models.CharField(max_length=100, verbose_name='Estación')

    def __str__(self):
        return "{} - {} [{}]".format(self.usuario.nombre_usuario, self.tabla, self.accion)
    
    class Meta:
        verbose_name = 'Auditoria Usuario'
        verbose_name_plural = 'Auditorias Usuarios'
        ordering = ('-fecha', 'hora')