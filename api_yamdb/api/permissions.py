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


class IsAuthorPermission(permissions.BasePermission):
    message = (
        'Доступ разрешен автору/модератору/администратору/суперпользователю.')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                )


class IsAdminPermission(permissions.BasePermission):
    message = 'Доступ разрешен только администратору или суперпользователю.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsReadOnlyPermission(permissions.BasePermission):
    message = 'Доступ разрешен только администратору или суперпользователю.'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
