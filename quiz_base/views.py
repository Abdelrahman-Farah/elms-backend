from django.conf import settings
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from dashboard.models import Course, CourseLearner

from .models import QuizModel
from .serializers import SimpleQuizModelSerializer, QuizModelSerializer
from .permissions import OwnerOrEnrolledRead



class QuizModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, OwnerOrEnrolledRead]
    serializer_class = SimpleQuizModelSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SimpleQuizModelSerializer

        user_id = self.request.user.id
        classroom_id = self.kwargs['course_pk']

        if user_id == Course.objects.select_related('owner').get(pk=classroom_id).owner.id:
            return QuizModelSerializer
        return SimpleQuizModelSerializer


    def get_queryset(self):
        return QuizModel.objects.filter(classroom = self.kwargs['course_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = serializer.save()

        classroom_id = self.kwargs['course_pk']
        classroom = Course.objects.get(pk=classroom_id)

        emails = []
        queryset = CourseLearner.objects.select_related('learner__user').filter(course=classroom)
        for course_learner in queryset:
            emails.append(course_learner.learner.user.email)

        try:
            send_mail(
                f'New Quiz in {classroom.title} classroom, About "{quiz.title}"',
                (
                    f'Description: {quiz.description}\n'
                    f'Time: {quiz.start_date}\n'
                    f'Duration: {quiz.duration_in_minutes}\n'
                ),
                settings.EMAIL_HOST_USER,
                emails,
                fail_silently=False,
            )
        finally:
            return Response(serializer.data, status=status.HTTP_201_CREATED)