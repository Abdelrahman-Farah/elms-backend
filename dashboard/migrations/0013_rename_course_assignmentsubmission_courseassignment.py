# Generated by Django 4.1.7 on 2023-05-11 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_rename_studentworkbook_assignmentsubmission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentsubmission',
            old_name='course',
            new_name='courseassignment',
        ),
    ]
