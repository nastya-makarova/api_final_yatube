from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class OwnerOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование или удаление объектов только автору.
    Всем прочим пользователям и анонимам информация должна быть доступна
    только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
