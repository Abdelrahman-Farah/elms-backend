from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "first_name", "last_name", "email", "username", "password"]


class UserSerializer(BaseUserSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "first_name", "last_name", "email", "username", "profile_picture"]
