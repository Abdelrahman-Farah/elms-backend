import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Contact, Chat
from core.models import User
import datetime
import time


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        
        Messages = Chat.objects.get(
            id=int(self.room_name)).messages.order_by('timestamp').all()
        
        participants = Chat.objects.get(
            id=int(self.room_name)).participants.all()
        # if the current user is not in the chat return empty list
        flag=False
        for participant in participants:
            if participant.user.username == data["from"]:
                flag=True
                break
        
        if not flag:
            return self.send_chat_message({
                "command": "fetch_messages",
                "messages": [],
            })
            
        content = {
            "command": "new_message",
            "messages": self.messages_to_json(Messages),
        }
        self.send_chat_message(content)

    def new_message(self, data):
        author_user = data["from"]
        user = User.objects.get(username=author_user)
        author_chat = Chat.objects.get(id=int(self.room_name))
        author_contact = Contact.objects.get(user=user)
        message = Message.objects.create(
            contact=author_contact,
            content=data["message"])
        author_chat.messages.add(message)

        content = {
            "command": "new_message",
            "message": self.message_to_json(message),
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        # print(result)
        return result

    def message_to_json(self,message):
        return {
            "author": message.contact.user.username,
            "content": message.content,
            "timestamp": str(message.timestamp),
        }

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # print(text_data)
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
