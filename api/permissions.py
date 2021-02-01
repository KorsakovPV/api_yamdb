"""
Описываются разрешения.

Определяем, должен ли запрос быть предоставлен или запрещен доступ.

"""

from rest_framework import permissions


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Класс разрешений IsAuthorAdminModeratorOrReadOnly."""

    def has_object_permission(self, request, view, obj):
        """
        Метод возвращает bool.

        Если запрос безопасный, только чтение ('GET', 'HEAD', 'OPTIONS') возврашает True.
        Если пользователь автор модератор или админ возвращает True.

        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user == obj.author or
                    request.user.is_moderator or
                    request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс разрешений IsAdminOrReadOnly."""

    def has_permission(self, request, view):
        """
        Метод возвращает bool.

        Если запрос безопасный, только чтение ('GET', 'HEAD', 'OPTIONS') возврашает True.
        Если пользователь админ возвращает True.

        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_admin

        return False


class IsAdmin(permissions.BasePermission):
    """Класс разрешений IsAdmin."""

    def has_permission(self, request, view):
        """
        Метод возвращает bool.

        Если пользователь админ возвращает True.

        """
        return request.user.is_authenticated and request.user.is_admin
