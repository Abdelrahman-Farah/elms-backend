import random
from rest_framework import serializers
from .models import Quiz, RandomQuestion
from quiz_base.models import QuizModel, DifficultySet, Question
from core.models import User

class CreateQuizSerializer(serializers.Serializer):
    quiz_model_id = serializers.IntegerField()

    def validate(self, data):
        quiz_model_id = data['quiz_model_id']
        user_id = self.context['user_id']

        if not QuizModel.objects.filter(pk=quiz_model_id).exists():
            raise serializers.ValidationError('The quiz you are trying to join does not exist.')

        if Quiz.objects.filter(quiz_model_id=quiz_model_id, user_id=user_id).exists():
            raise serializers.ValidationError('You can\'t take the quiz twice.')

        return data


    def save(self, **kwargs):
        quiz_model_id = self.validated_data['quiz_model_id']
        user_id = self.context['user_id']

        quiz = Quiz.objects.create(quiz_model_id=quiz_model_id, user_id = user_id)

        difficulty_sets = DifficultySet.objects.filter(quiz_model_id=quiz_model_id)

        for set in difficulty_sets:
            queryset = Question.objects.filter(set=set)

            all_questions_in_set = list(queryset)
            random.shuffle(all_questions_in_set)


            used_questions = all_questions_in_set[:set.number_of_used_questions_from_this_set]

            random_questions = [
                RandomQuestion(
                    quiz=quiz,
                    question=question
                ) for question in used_questions
            ]
            RandomQuestion.objects.bulk_create(random_questions)

        return quiz
