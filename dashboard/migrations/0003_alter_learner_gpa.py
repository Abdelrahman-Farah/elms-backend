# Generated by Django 4.1.7 on 2023-03-14 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_learner_gpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='GPA',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True),
        ),
    ]