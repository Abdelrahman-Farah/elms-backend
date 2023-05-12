from rest_framework_nested import routers
from . import views

from dashboard.urls import course_router

course_router.register(
    'assignments', views.CourseAssignmentViewSet, basename='course_assignment')

assignment_router = routers.NestedDefaultRouter(
    course_router, 'assignments', lookup='assignment')
assignment_router.register(
    'submissions', views.AssignmentSubmissionViewSet, basename='assignment_submission')


urlpatterns = assignment_router.urls
