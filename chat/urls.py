# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),

    # /contact/   -> list the contact of the user  {we need to provide a the user name and user profile picture and the user id and chat id and chat.back() }
    # /messages/chat-id  -> get the chat history of the chat room
    # /user/ -> list the users profile we have on the system
    # /create/chat/ -> create a chat room  ->  recive the id of the user that we need to chat with him -> return chat id

]
