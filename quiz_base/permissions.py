from rest_framework import permissions
from dashboard.models import Course, Learner, CourseLearner

class OwnerOrEnrolledRead(permissions.BasePermission):

    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')

        course = Course.objects.filter(id=course_id)
        if not course:
            return False
        if course[0].owner == request.user:
            return True


        if request.method in permissions.SAFE_METHODS:
            self.message = 'You are not registered in this Course.'

            learner = Learner.objects.filter(user = request.user)
            if not learner:
                return False

            return CourseLearner.objects.filter(course=course_id, learner=learner[0]).exists()
        else:
            self.message = 'You don\'t have the permisstion to create new quiz in this classroom.'
            return False