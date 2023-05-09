from rest_framework_nested.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('submit', views.SubmissionViewSet)
router.register('', views.TakeQuizViewSet)


# URLConf
urlpatterns = router.urls
