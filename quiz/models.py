from django.db import models
from quiz_base.models import QuizModel, Question
from django.conf import settings


class Quiz(models.Model):
    quiz_model = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "quizzes"
        unique_together = [['quiz_model', 'user']]

class RandomQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='random_questions')
    # TODO: cascade?
    question = models.ForeignKey(Question, on_delete=models.CASCADE)



class Submission(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=2)
