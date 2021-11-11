from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True, required=True)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Не заполенно поле Email'
            )
        if password is None:
            raise serializers.ValidationError(
                'Не заполенно поле Password'
            )
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с этим адресом электронной почты и паролем не найден.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Этот пользователь был деактивирован.'
            )
        update_last_login(None, user)
        return {'token': user.token, 'id': user.id}

    class Meta:
        model = User
