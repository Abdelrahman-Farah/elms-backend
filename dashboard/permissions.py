from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Course


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
        course = get_object_or_404(Course, id=course_id)
        return course.owner == request.user