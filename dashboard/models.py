from django.db import models
from django.conf import settings
import string
import random

# Create your models here.


# Define the Course model
class Course(models.Model):
    title = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="course-image", blank=True, null=True)
    join_code = models.CharField(max_length=7, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_owners"
    )

    # Override the save method of the Course model to generate a random join code
    def save(self, *args, **kwargs):
        if not self.join_code:
            while True:
                code = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=7)
                )
                if not Course.objects.filter(join_code=code).exists():
                    self.join_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["created_at"]


# Define the Learner model
class Learner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    GPA = models.DecimalField(max_digits=3, decimal_places=2, blank=True)

    # Override the save method of the Course model to generate a random GPA
    def save(self, *args, **kwargs):
        if not self.GPA:
            gpa = random.randint(180, 390)
            self.GPA = gpa/100

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        ordering = ["user"]


# Define the CourseLearner model
class CourseLearner(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="course_learners"
    )

    def __str__(self) -> str:
        return self.course.title

    class Meta:
        ordering = ["course", "learner"]


# Define the Post model
class Post(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="post-image", blank=True, null=True)
    file = models.FileField(upload_to="document-file", blank=True, null=True)
    video = models.FileField(upload_to="video", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="posts")

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["created_at"]


class CourseEvent(models.Model):
    event_id = models.CharField(max_length=255, null=True, blank=True)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="course_events")


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
