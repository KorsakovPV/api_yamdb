from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(max_length=300, blank=True)
    confirmation_code = models.CharField(max_length=6)
    description = models.TextField(max_length=300, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    role = models.CharField(max_length=9, choices=USER_ROLE, default='user')
