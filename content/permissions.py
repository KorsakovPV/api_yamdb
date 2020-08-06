from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # TODO gray елиф не нужен - выше и так ретерн
        elif request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')

# TODO red Пропущена часть OrReadOnly - хотелось бы, чтобы названия классов давали полное представление о том, что они делают
# ИМХО, не призываю менять - лично мне никогда не нравилось составлять вот такие большие условия в один класс, я всегда предпочитал делать маленькие простенькие пермишены и потом составлять в нужном порядке именно во вьюхах - так получалось более гибко.
class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    or request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (request.user.is_staff or request.user.role == 'admin' or
                    request.user.role == 'moderator' or
                    obj.author == request.user or
                    # TODO gray чтобы упросить вот такие выражения можно добавить property к модели юзеров вида is_moderator, которые будут возвращать Тру или Фолс как раз вот на такую проверку.
                    # В итоге здесь уменьшится количество кода и его станет проще читать. Тем более, уменьшится шанс на ошибку во время составления такого сложного логического условия
                    request.method == 'POST' and
                    request.user.is_authenticated):
                return True
        elif request.method in permissions.SAFE_METHODS:
            # TODO gray аналогично, только вот эту проверку лучше закинуть наверх - так мы не будем делать кучу лишних операций сравнений, если на самом деле у нас обычный гет-метод (python short circuiting)
            return True
