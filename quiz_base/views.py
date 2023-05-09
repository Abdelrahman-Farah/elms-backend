from rest_framework.viewsets import ModelViewSet
from .models import QuizModel, DifficultySet, Question
from .serializers import QuizModelSerializer, DifficultySetSerializer, QuestionSerializer

class QuizModelViewSet(ModelViewSet):
    queryset = QuizModel.objects.all()
    serializer_class = QuizModelSerializer


class DifficultySetViewSet(ModelViewSet):
    serializer_class = DifficultySetSerializer

    def get_queryset(self):
        return DifficultySet.objects.filter(quiz_model = self.kwargs['quiz_model_pk'])


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(set = self.kwargs['difficulty_set_pk'])