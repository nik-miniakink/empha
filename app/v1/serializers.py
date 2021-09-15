from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class ReadOnlyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active',
                  'last_login', 'is_superuser']


class WriteOnlyUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для методов с записью. Дополнительная валидация поля is_active
    """
    is_active = serializers.BooleanField(default=True)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password',
                  'is_active', 'is_superuser', 'last_login']

    def validate_is_active(self, value: bool) -> bool:
        print(value)
        if 'is_active' not in self.initial_data:
            raise serializers.ValidationError('This field is required.')
        return value

    def validate_password(self, value: str) -> str:
        """
        Хеширует пароль
        """
        return make_password(value)