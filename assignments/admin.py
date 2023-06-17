from django.contrib import admin
from .models import CourseAssignment,AssignmentSubmission

# Register your models here.
admin.site.register(CourseAssignment)
admin.site.register(AssignmentSubmission)