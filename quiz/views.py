import csv
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin

from dashboard.models import Course
from quiz_base.models import QuizModel

from .serializers import CreateRandomQuizSerializer, RandomQuizSerializer
from .serializers import NewSubmissionSerializer
from .serializers import ResultSerializer, SimpleQuizModelSerializer, AllResultsSerializer
from .models import Quiz
from .permissions import OwnerOrEnrolled, OwnerOnly


class TakeQuizViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, OwnerOrEnrolled]

    def get_queryset(self):
        user_id = self.request.user.id
        quiz_model_id = self.kwargs['quiz_model_pk']
        return Quiz.objects.filter(quiz_model=quiz_model_id, user=user_id)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateRandomQuizSerializer
        return RandomQuizSerializer

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            # Didn't take the quiz before
            return Response("", status=status.HTTP_204_NO_CONTENT)

        random_quiz_serializer = RandomQuizSerializer(self.get_queryset()[0])
        return Response(random_quiz_serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = CreateRandomQuizSerializer(
            data={},
            context = {
                'user_id': self.request.user.id,
                'classroom_id': self.kwargs['course_pk'],
                'quiz_model_id': self.kwargs['quiz_model_pk'],
            }
        )

        serializer.is_valid(raise_exception=True)
        quiz = serializer.save()

        serializer = RandomQuizSerializer(quiz)

        return Response(serializer.data, status=status.HTTP_200_OK)



class SubmitQuizViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, OwnerOrEnrolled]

    serializer_class = NewSubmissionSerializer

    def create(self, request, *args, **kwargs):
        quiz_model_id = self.kwargs['quiz_model_pk']
        queryset = QuizModel.objects.filter(pk=quiz_model_id)
        if not queryset:
            return Response('Quiz Model not found.', status=status.HTTP_404_NOT_FOUND)

        serializer = NewSubmissionSerializer(
            data=request.data,
            context = {
                'user_id': self.request.user.id,
                'classroom_id': self.kwargs['course_pk'],
                'quiz_model_id': self.kwargs['quiz_model_pk'],
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('You have submitted successfully.', status=status.HTTP_200_OK)




class QuizResultViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, OwnerOrEnrolled]

    def get_queryset(self):
        user_id = self.request.user.id
        quiz_model_id = self.kwargs['quiz_model_pk'],

        if user_id == Course.objects.select_related('owner').get(pk=self.kwargs['course_pk']).owner.id:
            return Quiz.objects.select_related('user').filter(quiz_model = quiz_model_id)

        return Quiz.objects.select_related('user').filter(quiz_model=quiz_model_id, user=user_id)


    def get_serializer_class(self):
        user_id = self.request.user.id
        if user_id == Course.objects.select_related('owner').get(pk=self.kwargs['course_pk']).owner.id:
            return AllResultsSerializer

        return ResultSerializer


    def list(self, request, *args, **kwargs):
        user_id = self.request.user.id

        is_owner = user_id == Course.objects.select_related('owner').get(pk=kwargs['course_pk']).owner.id
        if not is_owner and not self.get_queryset():
            # TODO: NO CONTENT?
            return Response({"detail": ['You didn\'t submit this quiz.']}, status=status.HTTP_204_NO_CONTENT)

        quiz_model_id = self.kwargs['quiz_model_pk'],
        quiz_model = QuizModel.objects.get(pk=quiz_model_id[0])
        quiz_model_serializer = SimpleQuizModelSerializer(quiz_model)

        if not is_owner:
            solutions_serializer = ResultSerializer(self.get_queryset()[0])
            response_data = {
                **quiz_model_serializer.data,
                **solutions_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            students_info = super().list(request, *args, **kwargs)

            response_data = {
                **quiz_model_serializer.data,
                "students_info": students_info.data
            }
            return Response(response_data, status=status.HTTP_200_OK)


class DownloadResultViewSet(ListModelMixin, GenericViewSet):

    permission_classes = [IsAuthenticated, OwnerOnly]

    def get_queryset(self):
        quiz_model_id = self.kwargs['quiz_model_pk'],
        return Quiz.objects.select_related('user').filter(quiz_model = quiz_model_id)


    def list(self, request, *args, **kwargs):
        quiz_model_id = self.kwargs['quiz_model_pk'],
        quiz_model = QuizModel.objects.get(pk=quiz_model_id[0])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=results of {quiz_model.title} quiz.csv'

        writer = csv.writer(response)
        writer.writerow(['Student Name', 'Email', 'Score'])

        queryset = self.get_queryset()
        for quiz in queryset:
            full_name = quiz.user.first_name + " " + quiz.user.last_name
            score_out_of_total = f'{quiz.score} / {quiz_model.total_grades_after_randomizing}'
            writer.writerow([full_name, quiz.user.email, score_out_of_total])

        return response