from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from api import serializers
from users.models import User

from api_yamdb.settings import CONFORMATION_SUBJECT, CONFORMATION_MESSAGE, SEND_FROM_EMAIL


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = serializers.UserEmailRegistration(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        user = User.objects.get_or_create(email=email)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        send_mail(CONFORMATION_SUBJECT,
                  f'{CONFORMATION_MESSAGE} {confirmation_code}',
                  SEND_FROM_EMAIL,
                  [email])
        return Response(f'The code was sent to the address {email}',
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = serializers.UserConfirmation(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        user = get_object_or_404(User, email=email)
        if request.user.is_authenticated():
            token = tokens.AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Invalid confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
