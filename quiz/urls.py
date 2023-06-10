from rest_framework_nested.routers import NestedDefaultRouter
from quiz_base.urls import course_router
from . import views

quiz_model_router = NestedDefaultRouter(course_router, 'quiz-model', lookup=  'quiz_model')

quiz_model_router.register('take', views.TakeQuizViewSet, basename = 'quiz-take')
quiz_model_router.register('submit', views.SubmitQuizViewSet, basename = 'quiz-submit')
quiz_model_router.register('result/download', views.DownloadResultViewSet, basename = 'quiz-result')
quiz_model_router.register('result', views.QuizResultViewSet, basename = 'quiz-result')

urlpatterns = quiz_model_router.urls
