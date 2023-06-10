from django.contrib import admin
from . import models


admin.site.register(models.QuizModel)
admin.site.register(models.DifficultySet)
admin.site.register(models.Question)
admin.site.register(models.Answer)
