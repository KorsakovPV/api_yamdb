from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    allowed_user_roles = ('admin',)

    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.role in self.allowed_user_roles

    # if request.user.is_authenticated:
    #     return bool(request.user.is_staff or request.user.role == 'admin')
    # TODO red как раз один из моментов, который значительно улучшится,
    #  если роли выделить в отдельный класс.
    # Сейчас у нас здесь идет сравнение со строкой, которая сама по себе
    # никакого смысла (семантического) не несет - здесь могла бы быть и
    # abra-cadabra и amdin.
    # Возможно, менеджеры решат, что админ это не звучит, нужно просто
    # переименовать роль - тогда будем бегать по всему проекту менять эти
    # строчки. А вдруг опечатка и все, не понятно почему код не работает.
    # Поэтому вот здесь сравнение с ролью хотелось бы увидеть как сравнение
    # с константой или полем класса
