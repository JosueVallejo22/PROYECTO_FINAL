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
    ESTADISTICA_CHOICES = [
        # Cualidad Tiro
        ('TIROS TOTALES', 'TIROS TOTALES'),
        ('TIROS AL ARCO', 'TIROS AL ARCO'),
        ('GOLES ANOTADOS', 'GOLES ANOTADOS'),
        ('PENALES EJECUTADOS', 'PENALES EJECUTADOS'),
        ('PENALES ANOTADOS', 'PENALES ANOTADOS'),
        
        # Cualidad Pase
        ('PASES TOTALES', 'PASES TOTALES'),
        ('PASES ACERTADOS', 'PASES ACERTADOS'),
        ('CENTROS TOTALES', 'CENTROS TOTALES'),
        ('CENTROS ACERTADOS', 'CENTROS ACERTADOS'),
        
        # Cualidad Velocidad
        ('SPRINT', 'SPRINT'),
        ('ACELERACION', 'ACELERACION'),
        
        # Cualidad Regate
        ('REGATES TOTALES', 'REGATES TOTALES'),
        ('REGATES EXITOSOS', 'REGATES EXITOSOS'),
        ('DUELOS TOTALES', 'DUELOS TOTALES'),
        ('DUELOS EXITOSOS', 'DUELOS EXITOSOS'),
        
        # Cualidad Defensa
        ('INTERCEPCIONES INTENTOS', 'INTERCEPCIONES INTENTOS'),
        ('INTERCEPCIONES EXITOSAS', 'INTERCEPCIONES EXITOSAS'),
        ('DUELOS DEFENSIVOS TOTALES', 'DUELOS DEFENSIVOS TOTALES'),
        ('DUELOS DEFENSIVOS GANADOS', 'DUELOS DEFENSIVOS GANADOS'),
        
        # Cualidad Fisico
        ('SALTO EVALUADO', 'SALTO EVALUADO'),
        ('DISTANCIA RECORRIDA', 'DISTANCIA RECORRIDA'),
        ('SPRINTS REALIZADOS', 'SPRINTS REALIZADOS'),
        ('FUERZA EXPLOSIVA EVALUADA', 'FUERZA EXPLOSIVA EVALUADA'),
        ('FUERZA ISOMETRICA EVALUADA', 'FUERZA ISOMETRICA EVALUADA'),
        ('FUERZA RESISTENCIA EVALUADA', 'FUERZA RESISTENCIA EVALUADA'),
        
        # Cualidad Manejo
        ('TIROS TOTALES RECIBIDOS', 'TIROS TOTALES'),
        ('TIROS BLOQUEADOS MANEJO', 'TIROS BLOQUEADOS'),
        ('DESPEJES TOTALES', 'DESPEJES TOTALES'),
        ('DESPEJES EXITOSOS', 'DESPEJES EXITOSOS'),
        ('BALONES ATRAPADOS', 'BALONES ATRAPADOS'),
        ('ATRAPES SIN REBOTE', 'ATRAPES SIN REBOTE'),
        
        # Cualidad Reflejo
        ('PENALES RECIBIDOS', 'PENALES RECIBIDOS'),
        ('PENALES ATAJADOS', 'PENALES ATAJADOS'),
        ('1V1 TOTALES', '1V1 TOTALES'),
        ('1V1 GANADOS', '1V1 GANADOS'),
        ('TIROS BLOQUEADOS REFLEJOS', 'TIROS BLOQUEADOS'),
        ('ATAJADAS CRITICAS REFLEJOS', 'ATAJADAS CRITICAS'),
        
        # Cualidad Saque
        ('SAQUES LARGOS INTENTOS', 'SAQUES LARGOS INTENTOS'),
        ('SAQUES LARGOS EXITOSOS', 'SAQUES LARGOS EXITOSOS'),
        ('SAQUES CORTOS INTENTOS', 'SAQUES CORTOS INTENTOS'),
        ('SAQUES CORTOS EXITOSOS', 'SAQUES CORTOS EXITOSOS'),
    ]

    estadistica = models.CharField(max_length=128, choices=ESTADISTICA_CHOICES, unique=True)
    cualidad = models.ForeignKey(Cualidad, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    descripcion = models.CharField(max_length=120, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Diccionario de mapeo de estadísticas a cualidades en mayúsculas
        estadisticas_a_cualidades = {
            # Cualidad Tiro
            'TIROS TOTALES': 'Tiro',
            'TIROS AL ARCO': 'Tiro',
            'GOLES ANOTADOS': 'Tiro',
            'PENALES EJECUTADOS': 'Tiro',
            'PENALES ANOTADOS': 'Tiro',
            
            # Cualidad Pase
            'PASES TOTALES': 'Pase',
            'PASES ACERTADOS': 'Pase',
            'CENTROS TOTALES': 'Pase',
            'CENTROS ACERTADOS': 'Pase',
            
            # Cualidad Velocidad
            'SPRINT': 'Velocidad',
            'ACELERACION': 'Velocidad',
            
            # Cualidad Regate
            'REGATES TOTALES': 'Regate',
            'REGATES EXITOSOS': 'Regate',
            'DUELOS TOTALES': 'Regate',
            'DUELOS EXITOSOS': 'Regate',
            
            # Cualidad Defensa
            'INTERCEPCIONES INTENTOS': 'Defensa',
            'INTERCEPCIONES EXITOSAS': 'Defensa',
            'DUELOS DEFENSIVOS TOTALES': 'Defensa',
            'DUELOS DEFENSIVOS GANADOS': 'Defensa',
            
            # Cualidad Fisico
            'SALTO EVALUADO': 'Fisico',
            'DISTANCIA RECORRIDA': 'Fisico',
            'SPRINTS REALIZADOS': 'Fisico',
            'FUERZA EXPLOSIVA EVALUADA': 'Fisico',
            'FUERZA ISOMETRICA EVALUADA': 'Fisico',
            'FUERZA RESISTENCIA EVALUADA': 'Fisico',
            
            # Cualidad Manejo
            'TIROS TOTALES RECIBIDOS': 'Manejo',
            'TIROS BLOQUEADOS MANEJO': 'Manejo',
            'DESPEJES TOTALES': 'Manejo',
            'DESPEJES EXITOSOS': 'Manejo',
            'BALONES ATRAPADOS': 'Manejo',
            'ATRAPES SIN REBOTE': 'Manejo',
            
            # Cualidad Reflejo
            'PENALES RECIBIDOS': 'Reflejos',
            'PENALES ATAJADOS': 'Reflejos',
            '1V1 TOTALES': 'Reflejos',
            '1V1 GANADOS': 'Reflejos',
            'TIROS BLOQUEADOS REFLEJOS': 'Reflejos',
            'ATAJADAS CRITICAS REFLEJOS': 'Reflejos',
            
            # Cualidad Saque
            'SAQUES LARGOS INTENTOS': 'Saque',
            'SAQUES LARGOS EXITOSOS': 'Saque',
            'SAQUES CORTOS INTENTOS': 'Saque',
            'SAQUES CORTOS EXITOSOS': 'Saque',
        }

        # Asignar la cualidad automáticamente según la estadística
        cualidad_nombre = estadisticas_a_cualidades.get(self.estadistica)
        if cualidad_nombre:
            self.cualidad = Cualidad.objects.get(cualidad=cualidad_nombre)
        else:
            raise ValueError(f"No se encontró una cualidad para la estadística '{self.estadistica}'.")

        super().save(*args, **kwargs)

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
    puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT, related_name="puesto_cualidades")
    cualidad = models.ForeignKey(Cualidad, on_delete=models.PROTECT)
    peso = models.DecimalField(max_digits=2, decimal_places=1)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.puesto} {self.cualidad} - {self.estado}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['puesto', 'cualidad'], name='unique_puesto_cualidad')
        ]
        verbose_name_plural = "Puestos - Cualidades"

    