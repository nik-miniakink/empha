from rest_framework import serializers

from .models import User


class ReadOnlyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser']


class WriteOnlyUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'is_active', 'is_superuser', 'last_login']

    def validate_is_active(self, value):
        if 'is_active' not in self.initial_data:
            raise serializers.ValidationError('This field is required.')
        return value
