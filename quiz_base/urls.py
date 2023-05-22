from rest_framework_nested.routers import NestedDefaultRouter
from dashboard.urls import router
from . import views


course_router = NestedDefaultRouter(router, 'course', lookup = 'course')

course_router.register('quiz-model', views.QuizModelViewSet, basename = 'classroom-quiz_model')


from quiz.urls import urlpatterns as quiz_patterns

urlpatterns = course_router.urls + quiz_patterns
