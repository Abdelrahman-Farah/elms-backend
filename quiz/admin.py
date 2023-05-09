from django.contrib import admin
from . import models


admin.site.register(models.Quiz)
admin.site.register(models.RandomQuestion)
admin.site.register(models.Submission)
