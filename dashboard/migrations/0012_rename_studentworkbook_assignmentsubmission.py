# Generated by Django 4.1.7 on 2023-05-11 20:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0011_rename_course_assignment_studentworkbook_course'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentWorkBook',
            new_name='AssignmentSubmission',
        ),
    ]
