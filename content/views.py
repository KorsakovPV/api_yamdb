from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Comment, Review, Title
from .permissions import IsAuthorOrAdminOrModerator
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        if title and serializer.is_valid:
            review = Review.objects.filter(title=title,
                                           author=self.request.user)
            if len(review) == 0:
                # TODO red Никогда не делайте len() от квайрисета. Если нужно проверить его длину, то есть готовый метод
                # Если посмотреть чуть шире, здесь не нужно этого делать вообще - нужно просто сделать правильный get_object_or_404
                serializer.save(author=self.request.user, title=title)
            else:
                raise ValidationError('Ревью не найдены')
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        # TODO red Не самая лучшая идея хранить рейтинг напрямую в модели - уж очень много головной боли по поводу поддержания настоящего значения при всех операциях удаления/добавления/изменения. Еще более неприятная идея работать с другой моделью, когда мы обращаемся к ревью - уж очень неочевидное поведение
        # Намного лучше подсчитывать рейтинг именно в тот момент, когда он нужен - во вьюсете тайтлов.
        title.rating = int_rating['score__avg']
        title.save(update_fields=['rating'])

    def perform_update(self, serializer):
        # TODO red в идеале этого метода не должно быть вообще, о чем я и говорил - головная боль
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=['rating'])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrModerator, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        # TODO red Комменты зависят от ревью, ревью от тайтла, значит комменты зависят и от ревью, и от тайтла. Поэтому нужно проверить, что в запросе валидно указаны оба этих параметра - коммент принадлежит ревью, который принадлежит тайтлу
        # Челлендж - сделать это одним get_object_or_404
        # Не забываем, что в кваргах не всегда бывает то, что нужно
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        # TODO red Аналогично
        if serializer.is_valid:
            # TODO red Эта строчка всегда дает Тру, потому что метод не вызван, а так как он существует, что ссылка на него дает Тру. Ну и про ифы в валидации сериализатроа уже говорил
            serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        if self.request.user.is_anonymous:
            # TODO red А зачем нужен этот метод?
            # В пермишене есть рид_онли (для безопасных), а методы обновления нифига не безопасные, поэтому сюда дойдут только не аноны
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
