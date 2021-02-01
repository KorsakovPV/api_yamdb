"""Представления."""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt import tokens

from api import serializers
from api.filters import TitleFilter
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorAdminModeratorOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer
)
from api_yamdb.settings import (
    CONFORMATION_MESSAGE,
    CONFORMATION_SUBJECT,
    SEND_FROM_EMAIL
)
from content.models import Category, Comment, Genre, Review, Title
from users.models import User


@api_view(['POST'])
def send_confirmation_code(request):
    """Эмуляция отправки кода подтверждения."""
    serializer = serializers.UserEmailRegistration(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    user = User.objects.get_or_create(email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(CONFORMATION_SUBJECT,
              f'{CONFORMATION_MESSAGE} {confirmation_code}',
              SEND_FROM_EMAIL,
              [email])
    return Response(f'The code was sent to the address {email}',
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    """Отправка token."""
    serializer = serializers.UserConfirmation(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = tokens.AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Invalid confirmation code'},
                    status=status.HTTP_400_BAD_REQUEST)


class ModelMixinSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                    GenericViewSet):
    """Класс ModelMixinSet. Промежуточный класс для дальнейшего наследования."""

    pass


class CategoryViewSet(ModelMixinSet):
    """Класс категория. Не полный ModelViewSet."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    """Класс жанр. Не полный ModelViewSet."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Класс заголовок. Не полный ModelViewSet."""

    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Возвращает класс, который должен использоваться для сериализатора."""
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        """Возвращает запрос для заголовка."""
        return Title.objects.annotate(
            rating=Avg('titles_reviews__score')).all()


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс отзыва."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Возвращает запрос для отзыва."""
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        """Вызывается CreateModelMixin при сохранении нового экземпляра объекта."""
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс комментария."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Возвращает запрос для комментариев."""
        review = get_object_or_404(Review,
                                   pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        """Вызывается CreateModelMixin при сохранении нового экземпляра объекта."""
        review = get_object_or_404(Review,
                                   pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """Класс пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin | IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    @action(methods=['patch', 'get'],
            permission_classes=[IsAuthenticated],
            detail=False,
            url_path='me',
            url_name='me')
    def me(self, request, *args, **kwargs):
        """PATCH-запрос на /users/me/ для заполнения поля в своём профайле."""
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
