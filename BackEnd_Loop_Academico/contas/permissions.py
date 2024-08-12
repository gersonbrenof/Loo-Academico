from rest_framework.permissions import BasePermission

class IsAdminOrAuthenticated(BasePermission):
    """
    Permissão que permite o acesso total aos administradores e 
    aos usuários autenticados as permissões normais.
    """

    def has_permission(self, request, view):
        # Permite o acesso total se o usuário for um administrador
        if request.user and request.user.is_staff:
            return True
        
        # Permite o acesso se o usuário estiver autenticado
        return request.user and request.user.is_authenticated
