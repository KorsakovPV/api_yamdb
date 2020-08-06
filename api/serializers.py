from rest_framework import serializers

# TODO green Мне нравится, что есть сериализаторы для таких запросов, но я бы назвал их как UserEmailRegistration и UserConfirmation. Но можно оставить и так, тоже хорошо
class SendConfirmationCodeSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)


class GetJwtTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
