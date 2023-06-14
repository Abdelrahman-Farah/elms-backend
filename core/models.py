from django.contrib.auth.models import AbstractUser
from django.db import models


class Creds(models.Model):
    has_gmail = models.BooleanField(default=False)
    code = models.CharField(max_length=255, null=True, blank=True)
    Gaccess_token = models.CharField(max_length=255, null=True, blank=True)
    Grefresh_token = models.CharField(max_length=255, null=True, blank=True)


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    creds = models.ForeignKey(
        Creds, on_delete=models.CASCADE, default=1, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile-picture", default='default.jpg')
