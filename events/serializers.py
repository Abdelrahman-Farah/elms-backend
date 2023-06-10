from rest_framework import serializers
from .models import CourseEvent


class CourseEventSerializer(serializers.ModelSerializer):
    event_id = serializers.CharField(read_only=True)

    class Meta:
        model = CourseEvent
        fields = ['id', 'event_id', 'summary', 'description',
                  'start_time', 'end_time']


class UserEventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='summary')
    start = serializers.DateTimeField(source='start_time')
    end = serializers.DateTimeField(source='end_time')

    class Meta:
        model = CourseEvent
        fields = ['id', 'title', 'start', 'end']
