from rest_framework import permissions
from dashboard.models import Course, Learner, CourseLearner

class OwnerOnly(permissions.BasePermission):
    """
    Custom permission class to only allow owners of a course to create posts related to that course.
    """
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')
        course = Course.objects.filter(id=course_id)
        return course[0].owner == request.user

class OwnerOrEnrolled(permissions.BasePermission):

    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')

        course = Course.objects.filter(id=course_id)
        if not course:
            return False
        if course[0].owner == request.user:
            return True


        learner = Learner.objects.filter(user = request.user)
        if not learner:
            return False

        return CourseLearner.objects.filter(course=course_id, learner=learner[0]).exists()