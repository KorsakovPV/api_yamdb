from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


def validate_year(year):
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError(
            f'title cannot be created later than {current_year}')


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='genre name')
    slug = models.SlugField(max_length=30, unique=True,
                            verbose_name='genre slug')

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='category name')
    slug = models.SlugField(max_length=30, unique=True,
                            verbose_name='category slug')

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'


class Title(models.Model):
    name = models.CharField(max_length=255, verbose_name='title name')
    year = models.IntegerField(validators=[validate_year],
                               default=0,
                               verbose_name='year of creation', db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category_titles', null=True,
                                 verbose_name='category')
    genre = models.ManyToManyField(Genre, related_name='genre_titles',
                                   blank=True, verbose_name='genre')
    description = models.TextField(blank=True,
                                   verbose_name='title description')

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return f'{self.pk} - {self.name[:20]} - {self.category}'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='titles_reviews')
    text = models.TextField(verbose_name='review text')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_reviews',
                               verbose_name='review author')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='title score')
    pub_date = models.DateTimeField(verbose_name='date published',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.pk} - {self.author} - {self.text[:20]}'


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='review_comments',
                               verbose_name='commented review')
    text = models.TextField(verbose_name='comment text')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_comments',
                               verbose_name='comment author')
    pub_date = models.DateTimeField(verbose_name='date published',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.pk} - {self.author} - {self.text[:20]}'
