# Generated by Django 4.1.7 on 2023-03-18 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_base', '0005_rename_total_grades_quizmodel_total_grades_after_randomizing'),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RandomizedQuestion',
            new_name='RandomQuestion',
        ),
    ]