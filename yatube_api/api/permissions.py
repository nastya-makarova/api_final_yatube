from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class OwnerOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование или удаление объектов только автору.
    Всем прочим пользователям и анонимам информация должна быть доступна
    только для чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    """Разрешение на получение информации анонимным пользователем."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ReadOnlyForGroups(permissions.BasePermission):
    """Разрешение для групп.
    Пользователь может только получать информацию о группах.
    Создание, изменение и удаление групп запрещены.
    """
    def check_safe_method(self, method):
        if method not in permissions.SAFE_METHODS:
            raise MethodNotAllowed('POST, PUT, PATCH, DELETE')

    def has_permission(self, request, view):
        self.check_safe_method(request.method)
        return True

    def has_object_permission(self, request, view, obj):
        self.check_safe_method(request.method)
        return True
