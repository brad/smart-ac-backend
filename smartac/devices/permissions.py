from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated devices.
    """

    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'auth_token'))
