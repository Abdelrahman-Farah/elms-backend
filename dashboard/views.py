from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin,DestroyModelMixin

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from .permissions import IsOwnerOrReadOnly, OwnerOnly
from .serializers import CourseEnrollSerializer, CourseLearnerSerializer, CourseSerializer, PostSerializer
from .models import Course, CourseLearner, Post, Learner


# Create your views here.

# Viewset for managing courses
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

    # Set permissions for the viewset based on the action being performed.
    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    # Get a queryset of all courses owned by the authenticated user and courses they are subscribed to.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Course.objects.filter(
                Q(owner=user) | Q(course_learners__learner__user=user)
            ).distinct()
            print(queryset)
            return queryset
        return Course.objects.none()

    # Return a list of all courses owned by the authenticated user and courses they are subscribed to.
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        owner_courses = queryset.filter(owner=request.user)
        
        learner_courses = queryset.exclude(owner=request.user)

        first_serializer = CourseSerializer(owner_courses, many=True)
        second_serializer = CourseSerializer(learner_courses, many=True)

        response_data = {
            "owner_courses": first_serializer.data,
            "learner_courses": second_serializer.data,
        }

        return Response(response_data)

    # Delete a course. Only the course owner can delete a course or a course learner can unsubscribe a course.
    def perform_destroy(self, instance):
        user = self.request.user
        course_learner = CourseLearner.objects.filter(
            course=instance, learner__user=user
        )
        if course_learner.exists():
            course_learner.delete()
        if user == instance.owner:
            instance.delete()

    # Create a new course owned by the authenticated user.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

# Viewset for managing posts
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    # Get the posts queryset based on the course id provided in the URL
    def get_queryset(self):
        course_id = self.kwargs["course_pk"]
        queryset = Post.objects.filter(course_id=course_id)
        return queryset

    # Create a new post for a given course
    def create(self, request, course_pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = get_object_or_404(Course, id=course_pk)
        serializer.save(owner=request.user, course=course)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

# Viewset for managing course enrollments
class CourseEnrollViewSet(CreateModelMixin, GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseEnrollSerializer
    permission_classes = [IsAuthenticated]

    # create method to handle course enrollment requests
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        join_code = serializer.validated_data.get("join_code")
        try:
            course = Course.objects.get(join_code=join_code)
        except Course.DoesNotExist:
            return Response(
                {"error": "Invalid enroll code"}, status=status.HTTP_400_BAD_REQUEST
            )

        learner, created = Learner.objects.get_or_create(user=request.user)
        if created:
            learner.save()

        if CourseLearner.objects.filter(learner=learner, course=course).exists():
            return Response({"detail": "User is already subscribed to this course."})

        subscribers = CourseLearner(learner=learner, course=course)
        subscribers.save()
        return Response({"detail": f"Successfully enrolled in course"})

# Viewset for Course Learner
class CourseLearnerViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CourseLearnerSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    # Get the Learners queryset based on the course id provided in the URL
    def get_queryset(self):
        course_id = self.kwargs["course_pk"]
        queryset = CourseLearner.objects.filter(course_id=course_id).select_related('learner__user')
        return queryset
