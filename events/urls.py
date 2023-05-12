from rest_framework import routers
from dashboard.urls import course_router
from . import views


course_router.register('events', views.CourseEventViewSet,
                       basename='course_event')

urlpatterns = course_router.urls
