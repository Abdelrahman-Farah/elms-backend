# Generated by Django 4.1.7 on 2023-03-09 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DifficultySet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_mandatory', models.BooleanField(default=False)),
                ('number_of_used_questions_from_this_set', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('start_date', models.DateTimeField()),
                ('duration_in_minutes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=512)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizzes.difficultyset')),
            ],
        ),
        migrations.AddField(
            model_name='difficultyset',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='difficulty_sets', to='quizzes.quiz'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=64)),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quizzes.question')),
            ],
        ),
    ]