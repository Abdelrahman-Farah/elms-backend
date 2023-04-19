from django.urls import include, path
from rest_framework_nested import routers
from . import views

router=routers.DefaultRouter()
router.register('course', views.CourseViewSet, basename='course')
router.register('enrollments', views.CourseEnrollViewSet, basename= 'course-enrollments')

course_router= routers.NestedDefaultRouter(router, 'course', lookup='course')
course_router.register('post', views.PostViewSet, basename= 'course_post')
course_router.register('learners', views.CourseLearnerViewSet, basename= 'course_learner')


urlpatterns =router.urls+course_router.urls