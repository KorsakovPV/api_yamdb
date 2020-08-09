import random
import string
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from api import serializers
from users.models import User

import api_yamdb.settings as s

import uuid


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = serializers.UserEmailRegistration(data=request.data)
    # TODO red почему из реквеста, если есть сериализатор? До проверки
    #  валидности вообще не стоит брать данные в руки
    if serializer.is_valid():
        email = serializer.data.get('email')
        user = User.objects.get_or_create(email=email)
        # TODO red get_or_create, так как у нас нет способа получать новый
        #  токен через рефреш, поэтому будем выкручиваться
        # TODO red уменьшаем вложенность, в этом методе это критично
        # confirmation_code = uuid.uuid4()

        # TODO red 1 - есть такая классная штука, UUID. Что это такое,
        #  почитайте сами, но вот вместо самопального генератора можно было
        #  взять UUID3/4
        confirmation_code = default_token_generator.make_token(user)
        # 2 - можно вообще не заморачиваться с хранением кода в юзере - в
        # джанго есть встроенный генератор для ссылок сбора паролей, он же
        # используется как default_token_generator. И самое классное в нем то,
        # что он может по юзеру сделать код, а потом по самому коду и юзеру
        # проверить, что код ему подходит - никаких дополнительных полей в
        # самом юзере
        # Выбрать любой из вариантов по вкусу
        user.confirmation_code = confirmation_code
        # TODO gray Всякие емейл настройки лучше выносить в сеттинги, а здесь
        #  брать их оттуда. Это более гибкое решение, дает возможность
        #  переиспользовать сообщения и не пользоваться "магическими
        #  константами"
        send_mail(s.CONFORMATION_SUBJECT,
                  f'{s.CONFORMATION_MESSAGE} {confirmation_code}',
                  s.SEND_FROM_EMAIL,
                  [email])
        return Response(f'The code was sent to the address {email}',
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = serializers.UserConfirmation(data=request.data)
    if serializer.is_valid():
        # TODO gray аналогично
        email = serializer.data.get('email')
        user = get_object_or_404(User, email=email)
        if request.user.is_authenticated():
            # TODO gray вот это место тоже нужно будет поменять после смены на
            #  нормальную генерилку кодов
            token = tokens.AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Invalid confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
