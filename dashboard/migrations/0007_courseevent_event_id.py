# Generated by Django 4.1.7 on 2023-04-23 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_courseevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseevent',
            name='event_id',
            field=models.CharField(default='none', max_length=255),
            preserve_default=False,
        ),
    ]
