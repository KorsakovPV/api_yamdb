from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', _('User')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Admin')
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(max_length=300, blank=True)
    confirmation_code = models.CharField(max_length=6, blank=True)
    description = models.TextField(max_length=300, blank=True)
    role = models.CharField(max_length=25,
                            choices=Role.choices,
                            default=Role.USER)
