# Generated by Django 4.1.7 on 2023-05-05 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_courseassignment_studentworkbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentworkbook',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]