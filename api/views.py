from django.contrib.auth.tokens import default_token_generator


from api import serializers
from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from content.models import Category, Comment, Genre, Review, Title
from django.contrib.auth.hashers import check_password, make_password

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt import tokens

from users.models import User

from api_yamdb.settings import CONFORMATION_SUBJECT, CONFORMATION_MESSAGE, SEND_FROM_EMAIL


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = serializers.UserEmailRegistration(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        user = User.objects.get_or_create(email=email)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        send_mail(CONFORMATION_SUBJECT,
                  f'{CONFORMATION_MESSAGE} {confirmation_code}',
                  SEND_FROM_EMAIL,
                  [email])
        return Response(f'The code was sent to the address {email}',
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = serializers.UserConfirmation(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        user = get_object_or_404(User, email=email)
        if request.user.is_authenticated():
            token = tokens.AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Invalid confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModelMixinSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                    GenericViewSet):
    pass


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('titles_reviews__score')).all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        if Review.objects.filter(author=self.request.user,
                                 title_id=title).exists():
            raise exceptions.ValidationError('Вы уже поставили оценку')
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        # Не забываем, что в кваргах не всегда бывает то, что нужно
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, review=review)
