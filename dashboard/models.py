from django.db import models
from django.conf import settings
import string, random

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="posts")

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["created_at"]

class PostFiles(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="document-file", blank=True, null=True)
    file_type = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.post.title

    class Meta:
        ordering = ["post"]