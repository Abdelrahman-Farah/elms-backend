# Generated by Django 4.1.7 on 2023-04-23 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_courseevent_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseevent',
            name='event_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
