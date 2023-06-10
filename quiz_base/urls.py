<<<<<<< HEAD
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
=======
from rest_framework_nested.routers import NestedDefaultRouter
from dashboard.urls import router
from . import views


course_router = NestedDefaultRouter(router, 'course', lookup = 'course')

course_router.register('quiz-model', views.QuizModelViewSet, basename = 'classroom-quiz_model')


from quiz.urls import urlpatterns as quiz_patterns

urlpatterns = course_router.urls + quiz_patterns
>>>>>>> a33b48bd02f73d46b04e9230a1e109de9eeca3b7
