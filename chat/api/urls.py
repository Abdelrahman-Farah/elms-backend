from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('chat', views.ChatViewSet, basename='chat')
router.register('contact', views.UserContactRetrive, basename='contact')
app_name = 'chat'

urlpatterns = router.urls
