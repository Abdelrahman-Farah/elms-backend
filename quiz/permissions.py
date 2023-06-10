from datetime import timedelta
from django.utils import timezone
from rest_framework import permissions

from dashboard.models import Course, Learner, CourseLearner
from quiz_base.models import QuizModel
from .models import Quiz

class OwnerOnly(permissions.BasePermission):
    """
    Custom permission class to only allow owners of a course to create posts related to that course.
    """
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')
        course = Course.objects.filter(id=course_id)
        return course[0].owner == request.user


class OwnerOrEnrolled(permissions.BasePermission):

    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')

        course = Course.objects.filter(id=course_id)
        if not course:
            return False
        if course[0].owner == request.user:
            return True


        learner = Learner.objects.filter(user = request.user)
        if not learner:
            return False

        return CourseLearner.objects.filter(course=course_id, learner=learner[0]).exists()



class ValidQuizInClassroom(permissions.BasePermission):
    def has_permission(self, request, view):
        classroom_id = view.kwargs.get('course_pk')
        quiz_model_id = view.kwargs.get('quiz_model_pk')

        queryset = QuizModel.objects.filter(pk = quiz_model_id)
        if not queryset:
            self.message = 'You are trying to access wrong quiz.'
            return False

        quiz_model = queryset[0]
        if str(quiz_model.classroom.id) != classroom_id:
            self.message = 'You are trying to access wrong quiz.'
            return False

        return True



class OnGoingQuiz(permissions.BasePermission):
    def has_permission(self, request, view):
        quiz_model_id = view.kwargs.get('quiz_model_pk')
        quiz_model = QuizModel.objects.get(pk = quiz_model_id)

        now = timezone.now()
        now = now.replace(tzinfo=timezone.utc).astimezone(tz=None)

        start_date = quiz_model.start_date
        end_date = start_date + timedelta(minutes=quiz_model.duration_in_minutes)

        if now < start_date:
            self.message = 'The quiz has not started yet!'
            return False

        if now >= end_date:
            self.message = 'Quiz deadline has already finished.'
            return False

        return True


class NotSubmittedBefore(permissions.BasePermission):
    def has_permission(self, request, view):
        queryset = Quiz.objects.filter(quiz_model=view.kwargs['quiz_model_pk'], user_id=request.user.id)
        if queryset:
            quiz = queryset[0]
            if quiz.is_submitted == True:
                self.message = 'You submitted this quiz before, You can\'t Take the quiz twice.'
                return False

        return True


class FinishedQuiz(permissions.BasePermission):
    def has_permission(self, request, view):
        quiz_model_id = view.kwargs.get('quiz_model_pk')
        quiz_model = QuizModel.objects.get(pk = quiz_model_id)

        now = timezone.now()
        now = now.replace(tzinfo=timezone.utc).astimezone(tz=None)

        start_date = quiz_model.start_date
        end_date = start_date + timedelta(minutes=quiz_model.duration_in_minutes)

        if now < end_date:
            self.message = 'The quiz has not finished yet, You can only see results when the quiz is finished.'
            return False

        return True
