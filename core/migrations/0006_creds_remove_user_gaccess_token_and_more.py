# Generated by Django 4.2.1 on 2023-06-10 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_merge_20230610_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('Gaccess_token', models.CharField(blank=True, max_length=255, null=True)),
                ('Grefresh_token', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='Gaccess_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='Grefresh_token',
        ),
        migrations.AddField(
            model_name='user',
            name='creds',
            field=models.OneToOneField(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.creds'),
        ),
    ]