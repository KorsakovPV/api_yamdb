from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    # TODO + red уже лучше, но это не внутренний под-класс в юзере, это отдельная
    #  сущность, поэтому просто этот класс нужно вынести наружу
    # TODO gray гет-текст нормальная тема, но сейчас вы себе просто
    #  усложнили работу немного
    USER = 'user', _('User')
    MODERATOR = 'moderator', _('Moderator')
    ADMIN = 'admin', _('Admin')


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(max_length=300, blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    description = models.TextField(max_length=300, blank=True)
    role = models.CharField(max_length=25,
                            choices=Role.choices,
                            default=Role.USER)

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff

    # TODO + red сравниваем не со строками, а Role.USER, например.
    #  Для модератора то же самое

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR
