from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()

router.register('course', views.CourseViewSet, basename='course')
router.register('enrollments', views.CourseEnrollViewSet,
                basename='course-enrollments')

course_router = routers.NestedDefaultRouter(router, 'course', lookup='course')
course_router.register('post', views.PostViewSet, basename='course_post')

post_router = routers.NestedDefaultRouter(course_router, 'post', lookup='post')
post_router.register('files', views.PostFilesViewSet, basename='post_files')

course_router.register(
    'learners', views.CourseLearnerViewSet, basename='course_learner')

course_router.register('is-owner', views.IsOwnerViewSet,
                       basename='course_is-owner')
from quiz_base.urls import urlpatterns as quiz_base_patterns
from events.urls import urlpatterns as event
from assignments.urls import urlpatterns as assignment

urlpatterns = router.urls + course_router.urls + \
    post_router.urls + quiz_base_patterns + assignment + event
