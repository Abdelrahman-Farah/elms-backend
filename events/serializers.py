from rest_framework import serializers
from .models import CourseEvent


class CourseEventSerializer(serializers.ModelSerializer):
    event_id = serializers.CharField(read_only=True)

    class Meta:
        model = CourseEvent
        fields = ['id', 'event_id', 'summary', 'description',
                  'start_time', 'end_time']
