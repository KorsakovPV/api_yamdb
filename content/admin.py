from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Genre, Title, Review, Comment

# Не обращайте внимания. Сейчас в админке есть возможность загрузки CSV\XLSX файлов, но она корявая.


class GenreAdmin(ImportExportModelAdmin):
    pass


class CategoryAdmin(ImportExportModelAdmin):
    pass


class TitleAdmin(ImportExportModelAdmin):
    pass


class ReviewAdmin(ImportExportModelAdmin):
    pass


class CommentAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
