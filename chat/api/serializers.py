from rest_framework import serializers
from chat.models import Chat, Contact
from core.models import User


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages']


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'user']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "profile_pic": obj.user.profile_picture.url,
        }
