from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


# # ИМХО, не призываю менять - лично мне никогда не нравилось составлять вот такие большие условия в один класс,
# # я всегда предпочитал делать маленькие простенькие пермишены и потом составлять в нужном порядке именно во вьюхах - так получалось более гибко.
# class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.method in permissions.SAFE_METHODS
#                     or request.user and request.user.is_authenticated)
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.user and request.user.is_authenticated:
#             if (request.user.is_staff or request.user.role == 'admin' or
#                     request.user.role == 'moderator' or
#                     obj.author == request.user or
#                     request.method == 'POST' and
#                     request.user.is_authenticated):
#                 return True
#
# # TODO gray чтобы упросить вот такие выражения можно добавить property к модели юзеров вида is_moderator, которые будут возвращать Тру или Фолс как раз вот на такую проверку.
# # В итоге здесь уменьшится количество кода и его станет проще читать. Тем более, уменьшится шанс на ошибку во время составления такого сложного логического условия
