class SessionUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el usuario está autenticado
        if request.session.get('user_id'):
            # Actualizar el tiempo de expiración de la sesión
            request.session.set_expiry(600)  # 10 minutos, o el tiempo que prefieras
            
        response = self.get_response(request)
        return response
