"""Модели приложения USERS."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    """Пользовательские роли."""

    # TODO gray гет-текст нормальная тема, но сейчас вы себе просто
    #  усложнили работу немного
    #  переделать на рранение в базе.
    USER = 'user', _('User')
    MODERATOR = 'moderator', _('Moderator')
    ADMIN = 'admin', _('Admin')


class User(AbstractUser):
    """Класс для хранения пользователей."""

    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(max_length=300, blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    description = models.TextField(max_length=300, blank=True)
    role = models.CharField(max_length=25,
                            choices=Role.choices,
                            default=Role.USER)

    @property
    def is_admin(self):
        """Метод возвращает True если пользователь админ."""
        return self.role == Role.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Метод возвращает True если пользователь модератор."""
        return self.role == Role.MODERATOR
