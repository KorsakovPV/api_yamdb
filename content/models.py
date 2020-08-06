from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
# TODO red Не лучший способ получать модель. Для этого есть get_user_model(). Это позволит достаточно безболезненно переехать на другую модель юзеров, например, при разделении на микросервисы

#TODO red Общий коммент - очень не хватает всяких улучшений вида verbose_name  для полей и для меты на целые классы. Это и как часть документации кода, и улучшение админки
class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    # TODO red стоп, а разве произведения искусства до нашей эры не существовали?
    # Как раз это прекрасно ложится в "отрицательный" год. Тем более, что "список категорий может быть расширен"
    # А вот валидировать то, что их год выпуска не больше, чем текущий, выглядит более хорошей идеей
    # Кстати, один из фильтров - по году, так что можно сделать из него индекс
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category_titles', null=True)
    genre = models.ManyToManyField(Genre, related_name='genre_titles',
                                   blank=True)
    description = models.TextField(blank=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.pk} - {self.name[:20]} - {self.category}'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='titles_reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_reviews')
    # TODO red а зачем здесь чойсы?
    # Мин/Макс валидаторы на месте, это хорошо, а интеджер это же ведь целочисленные значения, так что это здесь не нужно совсем
    score = models.IntegerField(
        choices=[(_, str(_)) for _ in range(1, 11)],
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.pk} - {self.author} - {self.text[:20]}'


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='review_comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_comments')
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.pk} - {self.author} - {self.text[:20]}'
