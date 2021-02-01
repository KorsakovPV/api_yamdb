"""Файлом конфигурации для самого приложения content."""
from django.apps import AppConfig


class ContentConfig(AppConfig):
    """
    Подключение приложения content.

    Для настройки приложения создаем класс наследник AppConfig и указываем
    путь для его импорта в INSTALLED_APPS.

    """

    name = 'content'
