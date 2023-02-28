from django.urls import path
from . import views

urlpatterns = [
    path('test2/', views.test),
]