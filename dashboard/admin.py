from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . import models

# Register your models here.

# Define an inline for the Post model to be displayed within CourseAdmin
class PostInline(admin.StackedInline):
    model = models.Post
    min_num = 0
    extra = 0

    # Override get_queryset method to return no objects initially
    def get_queryset(self, request):
        return models.Post.objects.none()

# Define an inline for the CourseLearner model to be displayed within CourseAdmin
class CourseLearnerInline(admin.StackedInline):
    model = models.CourseLearner
    min_num = 0
    extra = 0

    # Override get_queryset method to return no objects initially
    def get_queryset(self, request):
        return models.CourseLearner.objects.none()


# Define a custom admin class for the Course model
@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "created_at",
        "join_code",
        "get_learners_count",
        "get_posts_count",
    ]
    list_select_related = ["owner"]
    search_fields = ["title__istartswith", "course_Learner"]
    list_filter = ["created_at"]
    list_per_page = 10
    inlines = [CourseLearnerInline, PostInline]

    # Override get_queryset method to prefetch related objects for optimization
    def get_queryset(self, request):
        return (
            super().get_queryset(request).prefetch_related("posts", "course_learners")
        )

    # Define a custom method to display the number of learners in the course
    def get_learners_count(self, course):
        url = (
            reverse("admin:dashboard_courselearner_changelist")
            + f"?course_id={course.id}"
        )
        count = course.course_learners.count()
        return format_html(f'<a href="{url}">{count}</a>')

    # Define a custom method to display the number of learners in the course
    def get_posts_count(self, course):
        url = reverse("admin:dashboard_post_changelist") + f"?course_id={course.id}"
        count = course.posts.count()
        return format_html(f'<a href="{url}">{count}</a>')


# Define a custom admin class for the CourseLearner model
@admin.register(models.CourseLearner)
class CourseLearnerAdmin(admin.ModelAdmin):
    list_display = ["learner", "course"]
    list_filter = ["course"]
    list_select_related = ["course", "learner"]
    search_fields = ["course__istartswith"]
    list_per_page = 10


# Define a custom admin class for the Post model
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "course_title", "created_at"]
    list_filter = ["created_at", "course"]
    list_select_related = ["course"]
    search_fields = ["title__istartswith", "description__istartswith"]
    list_per_page = 10

    def course_title(self, Post):
        return Post.course.title


admin.site.register(models.Learner)
