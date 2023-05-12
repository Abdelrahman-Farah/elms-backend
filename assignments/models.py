from django.db import models
from django.conf import settings
from dashboard.models import Course


class CourseAssignment(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="document-file", blank=True, null=True)
    Image = models.ImageField(upload_to="post-image", blank=True, null=True)
    video = models.FileField(upload_to="video", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="assignments")
    degree = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["created_at"]


class AssignmentSubmission(models.Model):
    file = models.FileField(upload_to="document-file", blank=True, null=True)
    Image = models.ImageField(upload_to="post-image", blank=True, null=True)
    video = models.FileField(upload_to="video", blank=True, null=True)
    status = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    courseassignment = models.ForeignKey(
        CourseAssignment, on_delete=models.CASCADE, related_name="student_assignment")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_workbooks")

    def __str__(self) -> str:
        return self.student.first_name

    class Meta:
        ordering = ["time"]
