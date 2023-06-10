# Generated by Django 4.2.1 on 2023-05-11 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('quiz_base', '0005_rename_total_grades_quizmodel_total_grades_after_randomizing'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmodel',
            name='classroom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='dashboard.course'),
            preserve_default=False,
        ),
    ]
