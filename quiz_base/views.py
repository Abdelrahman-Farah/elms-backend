from rest_framework.viewsets import ModelViewSet
from .models import QuizModel, DifficultySet, Question
from .serializers import QuizModelSerializer, DifficultySetSerializer, QuestionSerializer

class QuizModelViewSet(ModelViewSet):
    queryset = QuizModel.objects.all()
    serializer_class = QuizModelSerializer

class DifficultySetViewSet(ModelViewSet):
    queryset = DifficultySet.objects.all()
    serializer_class = DifficultySetSerializer

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
