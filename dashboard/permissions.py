from rest_framework import permissions
from .models import Course,CourseLearner,Learner


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ 
        Custom permission class to allow owners to edit and view courses, 
        but only allow others to view courses.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'DELETE':
            return True
        return request.user == obj.owner
    


class OwnerOnly(permissions.BasePermission):
    """ 
    Custom permission class to only allow owners of a course to create posts related to that course.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        course_id = view.kwargs.get('course_pk')
        course = Course.objects.select_related('owner').filter(id=course_id)
        return course[0].owner == request.user
    

class EnrolledStudentsOnly(permissions.BasePermission):
    """
    Custom permission to allow only enrolled students to view the posts of a course.
    """
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')
        course = Course.objects.select_related('owner').filter(id=course_id)
        if not course:
            return False
        elif course[0].owner == request.user:
            return True
        learner = Learner.objects.filter(user = request.user)
        if not learner:
            return False
        return CourseLearner.objects.filter(course=course_id, learner=learner[0]).exists()
