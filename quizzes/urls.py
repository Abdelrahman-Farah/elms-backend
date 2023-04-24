from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('question', views.QuestionViewSet)

# URLConf
urlpatterns = router.urls
