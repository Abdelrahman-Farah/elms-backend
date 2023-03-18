from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views

router = DefaultRouter()
router.register('quiz-model', views.QuizModelViewSet)

quiz_model_router = NestedDefaultRouter(router, 'quiz-model', lookup='quiz_model')
quiz_model_router.register('difficulty', views.DifficultySetViewSet, basename='quiz-difficulty')

difficulty_set_router = NestedDefaultRouter(quiz_model_router, 'difficulty', lookup='difficulty_set')
difficulty_set_router.register('questions', views.QuestionViewSet, basename='difficulty-questions')

# URLConf
urlpatterns = router.urls + quiz_model_router.urls + difficulty_set_router.urls
