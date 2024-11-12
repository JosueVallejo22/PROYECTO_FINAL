from django.utils import timezone
from Aplicaciones.Login.models import Usuario

def obtener_usuario(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    
    try:
        return Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return None

def save_audit(request, model, action):
    from Aplicaciones.Auditoria.models import AuditoriaUsuario
    user = obtener_usuario(request)
    if not user:
        return
    
    #obtener direccion IP
    client_address = ip_client_address(request)

    #Registrar en la tabla de Auditorias en la base de datos
    auditusuariotabla = AuditoriaUsuario(usuario = user,
                                        tabla=model.__class__.__name__,
                                        registroid=model.id,
                                        accion=action,
                                        fecha=timezone.now().date(),
                                        hora=timezone.now().time(),
                                        estacion=client_address)
    auditusuariotabla.save()


    #Codigo para obtener el IP desde donde se realiza la accion

def ip_client_address(request):
    try:
        #case para servidor externo
        client_address = request.META['HTTP_X_FORWARDED_FOR']
    except KeyError:
        #case para localhost/servidor local
        client_address = request.META['REMOTE_ADDR']
    
    return client_address