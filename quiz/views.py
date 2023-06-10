from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from .models import Quiz, Submission
from .serializers import RandomQuizSerializer, TakeQuizSerializer, CreateSubmissionSerializer, SubmissionSerializer

class TakeQuizViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Quiz.objects.all()
    serializer_class = TakeQuizSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


    def create(self, request, *args, **kwargs):
        serializer = TakeQuizSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        quiz = serializer.save()

        serializer = RandomQuizSerializer(quiz)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = CreateSubmissionSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        serializer = CreateSubmissionSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        sumbission = serializer.save()

        serializer = SubmissionSerializer(sumbission)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
