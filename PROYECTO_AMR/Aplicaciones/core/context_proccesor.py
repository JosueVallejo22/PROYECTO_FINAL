# login/context_processors.py

from django.shortcuts import get_object_or_404
from Aplicaciones.Login.models import Usuario

def usuario_context_processor(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return {}  # Si no hay usuario, retorna un contexto vacío

    usuario = get_object_or_404(Usuario, id=user_id)
    es_admin = usuario.rol.rol == "ADMINISTRADOR"  # Verifica si el usuario es administrador
    return {'usuario': usuario, 'es_admin': es_admin}  # Agrega 'es_admin' al contexto

