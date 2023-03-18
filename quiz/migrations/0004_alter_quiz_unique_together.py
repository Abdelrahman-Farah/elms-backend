# Generated by Django 4.1.7 on 2023-03-18 10:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_base', '0005_rename_total_grades_quizmodel_total_grades_after_randomizing'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0003_alter_quiz_options_remove_quiz_score'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quiz',
            unique_together={('quiz_model', 'user')},
        ),
    ]
