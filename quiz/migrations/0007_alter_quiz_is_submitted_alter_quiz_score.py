# Generated by Django 4.2.1 on 2023-05-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_quiz_is_submitted_quiz_score_randomquestion_choice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='is_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
