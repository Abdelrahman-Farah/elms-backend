# Generated by Django 4.2.1 on 2023-06-11 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_user_has_gmail_creds_has_gmail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='creds',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.creds'),
        ),
    ]
