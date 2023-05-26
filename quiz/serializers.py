import random
from django.db import transaction
from rest_framework import serializers

from quiz_base.models import QuizModel, DifficultySet, Question, Answer

from .models import Quiz, RandomQuestion


############################ Create random quiz ############################
class CreateRandomQuizSerializer(serializers.Serializer):

    def validate(self, data):
        user_id = self.context['user_id']
        classroom_id = self.context['classroom_id']
        quiz_model_id = self.context['quiz_model_id']

        queryset = QuizModel.objects.filter(pk=quiz_model_id)
        if not queryset:
            raise serializers.ValidationError('The quiz you are trying to join does not exist.')

        quiz_model = queryset[0]
        if str(quiz_model.classroom.id) != classroom_id:
            raise serializers.ValidationError('The quiz you are trying to join does not exist in this classroom.')


        if Quiz.objects.filter(quiz_model_id=quiz_model_id, user_id=user_id).exists():
            raise serializers.ValidationError('You can\'t make two copies of the quiz.')

        return data


    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context['user_id']
            quiz_model_id = self.context['quiz_model_id']

            difficulty_sets = DifficultySet.objects.filter(quiz_model_id=quiz_model_id)

            quiz = Quiz.objects.create(quiz_model_id=quiz_model_id, user_id = user_id)

            random_questions = []
            for set in difficulty_sets:
                queryset = Question.objects.filter(set=set)

                all_questions_in_set = list(queryset)
                random.shuffle(all_questions_in_set)

                used_questions = all_questions_in_set[:set.number_of_used_questions_from_this_set]


                random_questions = random_questions + [
                    RandomQuestion(
                        quiz=quiz,
                        question=question
                    ) for question in used_questions
                ]
            random.shuffle(random_questions)
            RandomQuestion.objects.bulk_create(random_questions)
            return quiz
#################################################################################





############################ Serializing random quiz ############################
class SimpleAnswerSerializer(serializers.ModelSerializer):
    original_choice_id = serializers.IntegerField(source = 'id')
    class Meta:
        model = Answer
        fields = ['original_choice_id', 'body']


class RandomQuestionSerializer(serializers.ModelSerializer):
    random_question_id = serializers.SerializerMethodField()
    choices = SimpleAnswerSerializer(many = True, source='answers')

    def get_random_question_id(self, obj):
        return self.context['random_question_id']
    class Meta:
        model = Question
        fields = ['random_question_id', 'body', 'points', 'choices']

class RandomQuizSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 128, source='quiz_model.title')
    start_date = serializers.DateTimeField(source='quiz_model.start_date')
    duration_in_minutes = serializers.IntegerField(source='quiz_model.duration_in_minutes')
    total_points = serializers.DecimalField(max_digits=6, decimal_places=2, source='quiz_model.total_grades_after_randomizing')
    random_questions =  serializers.SerializerMethodField()

    def get_random_questions(self, obj):
        questions = []
        for random_question in obj.random_questions.all():
            serializer = RandomQuestionSerializer(
                random_question.question,
                context={
                    'random_question_id': random_question.id
                }
            )
            questions = questions + [serializer.data]

        return questions
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'start_date', 'duration_in_minutes', 'total_points', 'random_questions']
###############################################################################





############################ Submit quiz Solutions ############################
class RandomQuestionAndAnswerSerializer(serializers.Serializer):
    random_question = serializers.IntegerField()
    answer = serializers.IntegerField()

    def validate_random_question(self, value):
        quiz_id = self.context['quiz_id']
        queryset = RandomQuestion.objects.filter(pk=value)
        if not queryset:
            raise serializers.ValidationError('You are trying to answer wrong question.')

        random_question = queryset[0]
        if random_question.quiz.id != quiz_id:
            raise serializers.ValidationError('the question you are trying to answer does not exist in your random quiz.')

        return value

    def validate(self, data):
        queryset = RandomQuestion.objects.filter(pk=data['random_question'])
        if not queryset:
            raise serializers.ValidationError({"random_question": 'You are trying to answer wrong question.'})

        random_question = queryset[0]

        queryset = Answer.objects.filter(pk=data['answer'])
        if not queryset:
            raise serializers.ValidationError('There is no answer as the value provided.')

        answer = queryset[0]
        if answer.question != random_question.question:
            raise serializers.ValidationError('This choice is not a choice for the given random question.')
        return data


class NewSubmissionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    random_questions_and_answers = RandomQuestionAndAnswerSerializer(many = True)

    def validate_quiz_id(self, value):
        user_id = self.context['user_id']

        queryset = Quiz.objects.filter(pk=value, user_id=user_id)
        if not queryset:
            raise serializers.ValidationError('You are trying to answer wrong random quiz instance.')

        quiz = queryset[0]
        if quiz.is_submitted:
            raise serializers.ValidationError('You can not answer the quiz twice.')

        self.context.update({"quiz_id": value})
        return value


    def validate(self, data):
        random_question_ids = []
        for rq_a in data['random_questions_and_answers']:
            random_question_ids.append(rq_a['random_question'])

        if len(random_question_ids) > len(set(random_question_ids)):
            raise serializers.ValidationError('You can not answer the same question more than once.')
        return data


    def create(self, validated_data):
        with transaction.atomic():
            user_id = self.context['user_id']
            quiz_id = validated_data.pop('quiz_id')

            score = 0
            random_questions = []
            for rq_a in self.validated_data['random_questions_and_answers']:
                random_question = RandomQuestion.objects.get(pk=rq_a['random_question'])
                answer = Answer.objects.get(pk=rq_a['answer'])

                if answer.is_correct:
                    score += random_question.question.points

                random_question.choice = answer
                random_questions.append(random_question)

            RandomQuestion.objects.bulk_update(random_questions, ["choice"])

            quiz = Quiz.objects.get(pk=quiz_id, user_id=user_id)
            quiz.score = score
            quiz.is_submitted = True
            quiz.save()

            return quiz
###################################################################################





############################ Get Quiz results for one student ############################
class AnswerSerializer(serializers.ModelSerializer):
    chosen = serializers.SerializerMethodField()

    def get_chosen(self, obj):
        return self.context['chosen']
    class Meta:
        model = Answer
        fields = ['id', 'body', 'is_correct', 'chosen']

class QuestionChoiceSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        answers = []
        for answer in obj.answers.all():
            serializer = AnswerSerializer(
                answer,
                context = {
                    'chosen': self.context['choice'] == answer
                }
            )
            answers = answers + [serializer.data]
        return answers
    class Meta:
        model = Question
        fields = ['id', 'body', 'points', 'answers']


class ResultSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        questions = []
        for random_question in obj.random_questions.all():
            serializer = QuestionChoiceSerializer(
                random_question.question,
                context = {
                    'choice': random_question.choice
                }
            )
            questions = questions + [serializer.data]

        return questions

    class Meta:
        model = Quiz
        fields = ['score', 'questions']

###############################################################################




######################## Get Quiz results for whole classroom ########################
class SimpleQuizModelSerializer(serializers.ModelSerializer):
    quiz_model_id = serializers.IntegerField(source = 'id')
    total = serializers.DecimalField(max_digits=6, decimal_places=2, source='total_grades_after_randomizing')
    class Meta:
        model = QuizModel
        fields = ['quiz_model_id', 'title', 'description', 'start_date', 'duration_in_minutes', 'total']

class AllResultsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')


    def get_full_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    class Meta:
        model = Quiz
        fields = ['id', 'full_name', 'email', 'score']
###############################################################################