from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(max_length=300, blank=True)
    confirmation_code = models.CharField(max_length=6, default='000000')
    # TODO red Об этом поле см. коммент во вьюхе создания кода подтверждения. Либо это поле не нужно, либо его стоит сделать по-другому
    description = models.TextField(max_length=300, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # TODO red согласно доке email и username это разные поля модели юзера. Хорошая попытка упростить задачу, но в данном случае не подходит

    # TODO red Роль юзера, по факту, является отдельной сущностью. Их можно легко представить в отрыве от самих юзеров с различной дополнительной обработкой. Поэтому хорошо было бы вынести их как отдельный класс.
    # Но, так как у нас нет динамической составляющей (роли расписаны, во время работы добавляться/удаляться не будут), то стоит сделать не моделью. Подходящий класс поискать самостоятельно
    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    role = models.CharField(max_length=9, choices=USER_ROLE, default='user')
    # TODO red добавится через месяц новая роль под названием "супер-пупер-дупер админ", придется делать новую миграцию.
    # Пишем не под микроконтроллеры, байты считать не обязательно, поэтому лучше сразу взять с запасом длину чойса

    def create_user(self, email, password=None, **kwargs):
        # TODO red не понимаю, зачем это нужно, ведь такой метод есть уже у квайрисета юзеров, его вызова через super() , а еще тут какая-то работа с паролями, хотя паролей у нас нет
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
