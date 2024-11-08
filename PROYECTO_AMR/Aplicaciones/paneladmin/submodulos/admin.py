from django.contrib import admin
from Aplicaciones.paneladmin.submodulos.models import *
# Register your models here.
admin.site.register(Pais)
admin.site.register(Cualidad)
admin.site.register(Estadistica)
admin.site.register(Posicion)
admin.site.register(Puesto)
admin.site.register(PuestoCualidad)