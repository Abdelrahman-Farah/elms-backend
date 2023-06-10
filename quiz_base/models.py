from django.db import models

<<<<<<< HEAD

class QuizModel(models.Model):
=======
from dashboard.models import Course
from .managers import QuizModelManager

class QuizModel(models.Model):
    objects = QuizModelManager()
    classroom = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
>>>>>>> a33b48bd02f73d46b04e9230a1e109de9eeca3b7
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    duration_in_minutes = models.IntegerField()
    total_grades_after_randomizing = models.DecimalField(max_digits=6, decimal_places=2)


class DifficultySet(models.Model):
    quiz_model = models.ForeignKey(QuizModel, on_delete=models.CASCADE, related_name='difficulty_sets')
    is_mandatory = models.BooleanField(default=False)
    number_of_used_questions_from_this_set = models.IntegerField()


class Question(models.Model):
    body = models.CharField(max_length=512)
    set = models.ForeignKey(DifficultySet, on_delete=models.CASCADE, related_name='questions')
    points = models.DecimalField(max_digits=6, decimal_places=2)



class Answer(models.Model):
    body = models.CharField(max_length=64)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField()

    # def __str__(self) -> str:
    #     return f"Question: {self.question.body}, Choice: {self.body}"
