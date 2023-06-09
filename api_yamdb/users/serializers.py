from django.conf import settings
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        required=True,
        max_length=settings.USERNAME_MAX_LENGTH
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Недопустимый псевдоним "me"')
        return value

    def validate(self, value):
        username = value['username']
        email = value['email']
        if (User.objects.filter(
                email=email
        ).exclude(
            username=username
        ).exists() or User.objects.filter(
            username=username
        ).exclude(email=email).exists()):
            raise serializers.ValidationError({'email': 'Имя занято'})
        return value

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH
    )
