from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает вносить изменения только в свой профиль
    """
    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        return obj == request.user
