from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from users import permissions
from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]


class APIUser(APIView):
    # TODO Все это относится к юзерам, а вьюсет для них уже есть. Даже в урле это внутри одного ресурса /users/
    # Поэтому лучше отказаться от отдельной вьюхи и сделать это все кастомным экшеном внутри готового вьюсета
    def get(self, request):
        if request.user.is_authenticated:
            # TODO red это делается пермишеном
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('You are not authenticated',
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            # TODO red Это тоже
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                # TODO red в случаях, когда нет особой хитрой обработки ошибок сериализатора, намного проще и лучше писать не через иф, а прокинув параметр raise_exception, чтобы избежать лишней вложенности и ручной обработки ошибок
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('You are not authenticated',
                        status=status.HTTP_401_UNAUTHORIZED)
