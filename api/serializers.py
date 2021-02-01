"""Cериализаторы."""
from rest_framework import serializers

from content.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserEmailRegistration(serializers.Serializer):
    """Класс сериализатор Email."""

    email = serializers.EmailField(required=True)


class UserConfirmation(serializers.Serializer):
    """Класс сериализатор подтверждение Email."""

    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    """Класс сериализатор категории."""

    class Meta:
        """Мета класс. Определяем модель и поля модели."""

        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Класс сериализатор жанра."""

    class Meta:
        """Мета класс. Определяем модель и поля модели."""

        fields = ('name', 'slug',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Класс сериализатор заголовка для чтения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Мета класс. Определяем модель и поля модели."""

        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Класс сериализатор заголовка для записи."""

    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        """Мета класс. Определяем модель и поля модели."""

        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Класс сериализатор отзыва."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        """Мета класс. Определяем модель и поля модели."""

        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review

    def validate(self, data):
        """Пользователь может оставить только один отзыв на один объект."""
        if self.context['request'].method == 'PATCH':
            return data
        user = self.context['request'].user
        title = (self.context['request'].parser_context['kwargs']['title_id'])
        if Review.objects.filter(author=user, title_id=title).exists():
            raise serializers.ValidationError('Вы уже поставили оценку')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Класс сериализатор комментария."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        """Мета класс. Определяем модель и поля модели."""

        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатор пользователя."""

    class Meta:
        """Мета класс. Определяем модель и поля модели."""

        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role',)
