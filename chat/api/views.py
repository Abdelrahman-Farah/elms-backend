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
from .serializers import ChatSerializer, ContactSerializer


class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(participants__user=self.request.user).select_related("participants")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # get list of participants
        par = []
        participants = serializer.validated_data.get("participants")
        for p in participants:
            par.append(p.id)

        chat = Chat.objects.filter(participants__in=par).select_related("participants")

        # minimize the chat list to only chats with the same participants
        for p in participants:
            chat = chat.filter(participants=p)
        chat = chat.distinct()
        chat = chat.exists()
        if chat:
            return Response({"error": "Chat already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


class UserContactRetrive(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all().select_related("user")
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
