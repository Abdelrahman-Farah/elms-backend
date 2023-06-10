import random
from django.db import transaction
from rest_framework import serializers
from .models import Quiz, RandomQuestion, Submission
from quiz_base.models import QuizModel, DifficultySet, Question, Answer


class SimpleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'body']


class SimpleQuestionSerializer(serializers.ModelSerializer):
    answers = SimpleAnswerSerializer(many = True)
    class Meta:
        model = Question
        fields = ['id', 'body', 'points', 'answers']

class RandomQuestionSerializer(serializers.ModelSerializer):
    question = SimpleQuestionSerializer()
    class Meta:
        model = Question
        fields = ['question']

class RandomQuizSerializer(serializers.ModelSerializer):
    random_questions = RandomQuestionSerializer(many = True)
    class Meta:
        model = Quiz
        fields = ['id', 'random_questions']

class TakeQuizSerializer(serializers.Serializer):
    quiz_model_id = serializers.IntegerField()

    def validate(self, data):
        quiz_model_id = data['quiz_model_id']
        user_id = self.context['user_id']

        if not QuizModel.objects.filter(pk=quiz_model_id).exists():
            raise serializers.ValidationError('The quiz you are trying to join does not exist.')

        #TODO : erase comments
        if Quiz.objects.filter(quiz_model_id=quiz_model_id, user_id=user_id).exists():
            Quiz.objects.filter(quiz_model_id=quiz_model_id, user_id=user_id).delete()
            # raise serializers.ValidationError('You can\'t take the quiz twice.')

        return data


    def save(self, **kwargs):
        with transaction.atomic():
            quiz_model_id = self.validated_data['quiz_model_id']
            user_id = self.context['user_id']

            difficulty_sets = DifficultySet.objects.filter(quiz_model_id=quiz_model_id)

            quiz = Quiz.objects.create(quiz_model_id=quiz_model_id, user_id = user_id)

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

class QuestionAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    answer = serializers.IntegerField()

    def validate(self, data):
        print(self.context)
        return data
    pass

class CreateSubmissionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    questions_answers = QuestionAnswerSerializer(many = True)

    def validate(self, data):
        print(self.context)
        quiz_id = data['quiz_id']
        print(quiz_id)

        if not Quiz.objects.filter(pk=quiz_id, user_id=self.context['user_id']).exists():
            raise serializers.ValidationError('You are trying to answer wrong quiz.')

        quiz = Quiz.objects.filter(pk=quiz_id, user_id=self.context['user_id'])[0]
        if Submission.objects.filter(quiz=quiz).exists():
            raise serializers.ValidationError('You can not answer the quiz twice.')

        return data

    def save(self, **kwargs):
        quiz_id = self.validated_data['quiz_id']
        score = 0
        for qa in self.validated_data['questions_answers']:
            question = Question.objects.get(pk=qa['question'])
            answer = Answer.objects.get(pk=qa['answer'])
            if answer.is_correct:
                score += question.points

        submission = Submission.objects.create(quiz_id=quiz_id, score=score)
        return submission


class SubmissionSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    class Meta:
        model = Submission
        fields = ['id', 'quiz', 'total', 'score']

    def get_total(self, obj):
        print(obj)
        print(obj.quiz)
        print(obj.quiz.quiz_model)
        print(obj.quiz.quiz_model.total_grades_after_randomizing)
        return obj.quiz.quiz_model.total_grades_after_randomizing