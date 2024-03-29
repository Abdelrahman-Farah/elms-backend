from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    duration_in_minutes = models.IntegerField()


class DifficultySet(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='difficulty_sets')
    is_mandatory = models.BooleanField(default=False)
    number_of_used_questions_from_this_set = models.IntegerField()


class Question(models.Model):
    body = models.CharField(max_length=512)
    set = models.ForeignKey(DifficultySet, on_delete=models.CASCADE, related_name='questions')
    score = models.DecimalField(max_digits=5, decimal_places=2)



class Answer(models.Model):
    body = models.CharField(max_length=64)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField()

    # def __str__(self) -> str:
    #     return f"Question: {self.question.body}, Choice: {self.body}"
