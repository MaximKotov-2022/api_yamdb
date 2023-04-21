from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.user.is_authenticated
                and request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для пользователей с правами администратора или на чтение."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.method in permissions.SAFE_METHODS
                )