from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dashboard.models import Course
from dashboard.permissions import OwnerOnly
from .models import CourseAssignment, AssignmentSubmission
from .serializers import CourseAssignmentSerializer, AssignmentSubmissionSerializer, AssignmentSubmissionForOwnerSerializer


class CourseAssignmentViewSet(ModelViewSet):
    '''
    viewset for managing course assignments
        get: get all assignments for a course
        post: create a new assignment for a course
    '''
    serializer_class = CourseAssignmentSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def get_queryset(self):
        course_id = self.kwargs["course_pk"]
        queryset = CourseAssignment.objects.filter(
            course_id=course_id).select_related('course')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = kwargs['course_pk']
        course = get_object_or_404(Course, id=course_id)
        serializer.save(course=course)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AssignmentSubmissionViewSet(ModelViewSet):
    '''
    viewset for managing assignment submissions
        for owner of the course:
            get: get all submissions for an assignment
            list: get all submissions for a course
            update: update a submission
            destroy: delete a submission
            isOwner: check if the user is the owner of the course

        for learner:
            get: get all submissions for an assignment  (only for the learner who submitted)
            list: get all submissions for a course (only for the learner who submitted)
            create: create a new submission (only for the learner who submitted)
            update: update a submission (only for the learner who submitted)
            destroy: delete a submission (only for the learner who submitted)

    '''
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AssignmentSubmission.objects.filter(
            courseassignment_id=self.kwargs['assignment_pk']).\
            select_related('student').select_related('courseassignment')

        return queryset

    def isOwner(self, request, *args, **kwargs):
        owner = Course.objects.get(
            id=self.kwargs['course_pk']).owner
        return owner == request.user

    def get_serializer(self, *args, **kwargs):
        if self.isOwner(self.request, *args, **kwargs):
            return AssignmentSubmissionForOwnerSerializer(*args, **kwargs)
        else:
            return AssignmentSubmissionSerializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        if self.isOwner(request, *args, **kwargs):
            queryset = self.get_queryset()
            queryset = queryset.filter(
                status=True)
            serializer = AssignmentSubmissionForOwnerSerializer(
                queryset, many=True)
            return Response(serializer.data)
        else:
            (queryset, created) = self.get_queryset().get_or_create(
                student=request.user, courseassignment_id=kwargs['assignment_pk'])
            serializer = AssignmentSubmissionSerializer(queryset)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if not self.isOwner(request, *args, **kwargs) and request.user != self.get_object().student:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self.isOwner(request, *args, **kwargs):
            # check if the assignment is still open for submission or not (deadline passed)
            # if passed, return 403 forbidden
            assignment_deadline = CourseAssignment.objects.get(
                id=self.kwargs['assignment_pk']).due_date
            submession_time = timezone.now()
            if submession_time > assignment_deadline:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)