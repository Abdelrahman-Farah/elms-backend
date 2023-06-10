from . import views
from django.urls import path

urlpatterns = [
    path('jwt/create/', views.CustomUserLoginView.as_view()),
    path('users/reset_password/', views.CustomResetPasswordView.as_view())
]
