from django.contrib.auth.models import AbstractUser
from django.db import models

#i am here
class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)