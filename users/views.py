from django.contrib.auth import get_user_model

from rest_framework import filters, viewsets
from rest_framework.response import Response

from users import permissions
from users.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    @action(methods=['patch', 'get'],
            permission_classes=[IsAuthenticated],
            detail=False,
            url_path='me',
            url_name='me')
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
