from django.db import models

class QuizModelManager(models.Manager):
    def get_queryset(self):
        return super(QuizModelManager, self).get_queryset().prefetch_related('difficulty_sets__questions__answers')