from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework import filters
from chat.models import Chat, Contact
from .serializers import ChatSerializer, ContactSerializer, ChatSerializerForCreate


class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    
    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            return ChatSerializerForCreate(*args, **kwargs)
        else :
            return super().get_serializer(*args, **kwargs)
            
    
    def get_queryset(self):
            return Chat.objects.filter(participants__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # get list of participants
        par = []
        userCont=Contact.objects.filter(user=self.request.user)
        serializer.data['participants'].append(userCont[0].id)
        serializer.is_valid(raise_exception=True)
        
        participants = serializer.validated_data.get("participants")
        participants.append(userCont[0])
        for p in participants:
            par.append(p.id)
        
        chat = Chat.objects.filter(participants__in=par)

        # minimize the chat list to only chats with the same participants
        for p in participants:
            chat = chat.filter(participants=p)
        chat = chat.distinct()
        chat = chat.exists()
        
        if chat:
            return Response({"error": "Chat already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(participants)
            NewChat = Chat.objects.create()
            NewChat.participants.set(participants)
            NewChat.participants.add(userCont[0])
            NewChat.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


class UserContactRetrive(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    def get_queryset(self):
        # return all contacts exept the contact that participate in the user chat
        return Contact.objects.exclude(user=self.request.user).exclude(chats__participants__user=self.request.user).distinct()
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
   
                
    