from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

SCORE_CHOICES = list(zip(range(1, 10), range(1, 10)))


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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category_titles', )
    genre = models.ManyToManyField(Genre, related_name='genre_titles',
                                   blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.pk} - {self.name[:20]} - {self.category}'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='titles_reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_reviews')
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)

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

    def __str__(self):
        return f'{self.pk} - {self.author} - {self.text[:20]}'
