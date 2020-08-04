from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'year', 'category', 'description', 'rating')
    search_fields = ('name', )
    list_filter = ('year', 'category', 'rating', 'genre')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', )
    list_filter = ('author', 'score')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('text', )
    list_filter = ('review', 'author')
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
