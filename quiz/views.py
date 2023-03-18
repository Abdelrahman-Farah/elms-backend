from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import CreateQuizSerializer

class QuizViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Quiz.objects.all()
    serializer_class = CreateQuizSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
