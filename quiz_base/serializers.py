from django.db import transaction
from rest_framework import serializers
from .models import QuizModel, DifficultySet, Question, Answer


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
            raise serializers.ValidationError('This question has more than one correct choice.')

        return answers

    class Meta:
        model = Question
        fields = ['id', 'body', 'score', 'answers']


class DifficultySetSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many = True)

    def validate(self, data):
        if data['number_of_used_questions_from_this_set'] > len(data['questions']):
            raise serializers.ValidationError('The number of used questions from this set is greater than the actual number of questions.')

        if data['number_of_used_questions_from_this_set'] < 0:
            raise serializers.ValidationError('The number of used questions from this set must not be negative.')

        if data['is_mandatory'] == True and data['number_of_used_questions_from_this_set'] != len(data['questions']):
            raise serializers.ValidationError('This set is mandatory, So the number_of_used_questions_from_this_set must be equal to the number of all questions.')

        return data

    class Meta:
        model = DifficultySet
        fields = ['id', 'is_mandatory', 'number_of_used_questions_from_this_set', 'questions']



class QuizModelSerializer(serializers.ModelSerializer):
    difficulty_sets = DifficultySetSerializer(many = True)

    def validate_difficulty_sets(self, difficulty_sets):

        mandatory_sets = 0
        for set in difficulty_sets:
            mandatory_sets += set['is_mandatory']

        if mandatory_sets > 1:
            raise serializers.ValidationError('This quiz has more than one mandatory sets.')

        return difficulty_sets

    class Meta:
        model = QuizModel
        fields = ['id', 'title', 'description', 'start_date', 'duration_in_minutes', 'difficulty_sets']


    def create(self, validated_data):
        with transaction.atomic():

            difficulty_sets_data = validated_data.pop('difficulty_sets')
            quiz_model = QuizModel.objects.create(**validated_data)

            for difficulty_set_data in difficulty_sets_data:
                questions_data = difficulty_set_data.pop('questions')
                difficulty_set = DifficultySet.objects.create(quiz_model=quiz_model, **difficulty_set_data)

                for question_data in questions_data:
                    answers_data = question_data.pop('answers')
                    question = Question.objects.create(set=difficulty_set, **question_data)

                    answers = [
                        Answer(
                            question=question,
                            **answer,
                        ) for answer in answers_data
                    ]
                    Answer.objects.bulk_create(answers)

            return quiz_model
