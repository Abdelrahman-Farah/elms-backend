from django.db import transaction
from rest_framework import serializers
from .models import Quiz, DifficultySet, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'body', 'is_correct']



class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many = True)

    def validate_answers(self, answers):
        if len(answers) < 2:
            raise serializers.ValidationError('The question must have atleast 2 choices.')

        correct_answers = 0
        for answer in answers:
            correct_answers += answer['is_correct']

        if correct_answers == 0:
            raise serializers.ValidationError('This question has no correct answer.')

        if correct_answers > 1:
            raise serializers.ValidationError('This question have more than one correct choice.')

        return answers


    class Meta:
        model = Question
        fields = ['id', 'body', 'score', 'answers']

    def create(self, validated_data):
        with transaction.atomic():
            answers_dict = validated_data.pop('answers')

            # TODO: change the set
            question = Question.objects.create(set=DifficultySet.objects.get(pk=1), **validated_data)
            answers = [
                Answer(
                    question=question,
                    **answer,
                ) for answer in answers_dict
            ]
            Answer.objects.bulk_create(answers)
            return question


class DifficultySetSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many = True)
    class Meta:
        model = DifficultySet
        fields = ['id', 'is_mandatory', 'number_of_used_questions_from_this_set', 'questions']



class QuizSerializer(serializers.ModelSerializer):
    difficulty_sets = DifficultySetSerializer(many = True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'start_date', 'duration_in_minutes', 'difficulty_sets']
