from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from core.models import User

from .permissions import IsOwnerOrReadOnly, OwnerOnly
from .serializers import AssignmentSubmissionForOwnerSerializer, AssignmentSubmissionSerializer, CourseAssignmentSerializer, CourseEnrollSerializer, CourseLearnerSerializer, CourseSerializer, PostSerializer, LearnerSerializer, CourseEventSerializer
from .models import Course, CourseAssignment, CourseLearner, Post, Learner, CourseEvent, AssignmentSubmission

# Course Event Stuff
import json
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# TOP SECRET STUFF
CLIENT_ID = '299051002384-j2r35j9lhn9dq11u8f04qgjbg7bknm0c.apps.googleusercontent.com'
CLIENT_SECRET = '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'

# SCOPES for accessing calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']


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
        queryset = CourseLearner.objects.filter(
            course_id=course_id).select_related('learner__user')
        return queryset


class LearnerViewSet(ModelViewSet):
    queryset = Learner.objects.select_related('user').order_by('GPA').all()
    serializer_class = LearnerSerializer

####################################################### doma part ########################################################


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


class CourseEventViewSet(ModelViewSet):
    queryset = CourseEvent.objects.all()
    serializer_class = CourseEventSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def get_create_credentials(self):
        """
        Obtain Google OAuth2 credentials from authorization code.

        This method receives a `POST` request with a `code` parameter, which
        is used to obtain access and refresh tokens from the Google OAuth2
        endpoint. The access and refresh tokens are then stored in the current
        user's model instance for future use.

        Returns:
        A dictionary with the OAuth2 tokens.
        """

        # Get user and form data
        user = User.objects.get(id=self.request.user.id)
        url = 'https://oauth2.googleapis.com/token'
        REDIRECT_URI = 'http://localhost:3000'
        form_data = json.loads(self.request.body.decode())
        code = form_data.get('code')
        data = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        response = requests.post(url, data=data)
        token_data = response.json()
        user.Gaccess_token = token_data['access_token']
        user.Grefresh_token = token_data['refresh_token']
        user.has_gmail = True
        user.save()
        return response.json()

    def get_credentials(self):
        """
        Retrieve Google OAuth2 credentials from user model instance.

        This method retrieves the access and refresh tokens from the current
        user's model instance and returns a `Credentials` object that can be
        used to make requests to the Google Calendar API.

        Returns:
        A `Credentials` object.
        """

        # Get user
        user = User.objects.get(id=self.request.user.id)
        info = {
            'access_token': user.Gaccess_token,
            'refresh_token': user.Grefresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        credentials = Credentials.from_authorized_user_info(info, SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                return
        user.Grefresh_token = credentials.refresh_token
        user.save()
        return credentials

    def create(self, request, *args, **kwargs):
        """
        Creates a new event in the user's Google Calendar and saves the event information to the database.

        Args:
            request: The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            A Response object with the serialized data of the created event and a status code of 201 if the event was successfully created and saved.
            A Response object with a status code of 403 if the user's credentials are invalid.
            A Response object with a status code corresponding to the HTTP error returned by the Google Calendar API if there was an error creating the event.
        """

        # Validate serializer data and retrieve course information
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = kwargs['course_pk']
        course = get_object_or_404(Course, id=course_id)

        # Retrieve user credentials and check if they are valid
        credentials = self.get_credentials()
        if credentials.valid:
            # Retrieve attendee information and create event object for Google Calendar API
            attendees = []
            for attendee in CourseLearner.objects.filter(
                    course_id=course_id).select_related('learner__user'):
                attendees.append({'email': attendee.learner.user.email})

            service = build('calendar', 'v3', credentials=credentials)

            event = {
                'summary': serializer.validated_data['summary'],
                'description': serializer.validated_data['description'],
                "colorId": 10,
                'start': {
                    'dateTime': serializer.validated_data['start_time'].isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': serializer.validated_data['end_time'].isoformat(),
                    'timeZone': 'UTC',
                },
                'attendees': attendees,
            }

        # Create event in Google Calendar and save event information to database
            try:
                event = service.events().insert(calendarId='primary', body=event).execute()
                # save the event id to the database
                serializer.save(course=course, event_id=event['id'])
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))
            except requests.HTTPError as error:
                return Response(status=error.resp.status)

        return Response(
            status=status.HTTP_403_FORBIDDEN
        )

    def get_queryset(self):
        course_id = self.kwargs["course_pk"]
        queryset = CourseEvent.objects.filter(course_id=course_id)
        return queryset

    def perform_destroy(self, instance):
        # Get Google Calendar API credentials
        credentials = self.get_credentials()

        # Delete the corresponding event from the Google Calendar
        try:
            service = build('calendar', 'v3', credentials=credentials)
            service.events().delete(calendarId='primary', eventId=instance.event_id).execute()
        except:
            pass
        return super().perform_destroy(instance)
