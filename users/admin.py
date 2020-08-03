from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import User


class UserAdmin(ImportExportModelAdmin):
    pass


admin.site.register(User, UserAdmin)
