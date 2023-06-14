from django.db import models
from dashboard.models import Course


class CourseEvent(models.Model):
    event_id = models.CharField(max_length=255, null=True, blank=True)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_events")

    def __str__(self):
        return self.summary
