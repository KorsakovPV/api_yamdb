from rest_framework import serializers


class SendСonfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class GetJwtTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
