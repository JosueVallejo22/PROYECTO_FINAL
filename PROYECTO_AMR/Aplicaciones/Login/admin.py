from django.contrib import admin
from .models import Rol, Usuario

# Registra el modelo Rol
admin.site.register(Rol)
admin.site.register(Usuario)


# Registra el modelo Usuario (tu modelo personalizado)
# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ('nombre_usuario', 'nombre', 'apellido', 'correo', 'numero_telefono', 'estado', 'rol')
#     search_fields = ('nombre_usuario', 'correo', 'nombre', 'apellido')
#     list_filter = ('rol', 'estado')
