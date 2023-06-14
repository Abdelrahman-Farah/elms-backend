from django.contrib import admin

from .models import Message, Contact, Chat

admin.site.register(Message)
admin.site.register(Contact)
admin.site.register(Chat)
