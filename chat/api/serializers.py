from rest_framework import serializers
from chat.models import Chat, Contact
from core.models import User


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages']
        
    def get_participants(self, obj):
        return [
            {
                "id": p.user.id,
                "username": p.user.username,
                "email": p.user.email,
                "first_name": p.user.first_name,
                "last_name": p.user.last_name,
                "profile_pic": p.user.profile_picture.url,
            }
            for p in obj.participants.all()
        ]

class ChatSerializerForCreate(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'participants']
        


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
