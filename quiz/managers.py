from django.db import models


class QuizManager(models.Manager):
    def get_queryset(self):
        return super(QuizManager, self).get_queryset().select_related('quiz_model').prefetch_related('random_questions__question__answers')