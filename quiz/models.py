from django.db import models
from django.conf import settings

from quiz_base.models import QuizModel, Question, Answer

from .managers import QuizManager

class Quiz(models.Model):
    objects = QuizManager()
    quiz_model = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    is_submitted = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    class Meta:
        verbose_name_plural = "quizzes"
        unique_together = [['quiz_model', 'user']]


class RandomQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='random_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.OneToOneField(Answer, on_delete=models.CASCADE, null=True, blank=True)