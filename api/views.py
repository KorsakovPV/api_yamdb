import random
import string

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from api import serializers
from users.models import User


def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


# @api_view(['POST'])
# def send_confirmation_code(request):
#     serializer = serializers.SendСonfirmationCodeSerializer(data=request.data)
#     email = request.data['email']
#     if serializer.is_valid():
#         confirmation_code = id_generator()
#         user = User.objects.filter(email=email).exists()
#         if not user:
#             User.objects.create_user(email=email)
#         User.objects.filter(email=email).update(
#             confirmation_code=make_password(confirmation_code, salt=None,
#                                             hasher='default')
#         )
#         mail_subject = 'Confirmation code on Yamdb'
#         message = f'Your confirmation code: {confirmation_code}'
#         send_mail(mail_subject, message, 'Yamdb <admin@yamdb.ru>', [email])
#         return Response(f'The code was sent to the address {email}',
#                         status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = serializers.GetJwtTokenSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if check_password(confirmation_code, user.confirmation_code):
            token = tokens.AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Invalid confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
