"""Файлом конфигурации для самого приложения users."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Подключение приложения users.

    Для настройки приложения создаем класс наследник AppConfig и указываем
    путь для его импорта в INSTALLED_APPS.

    """

    name = 'users'
