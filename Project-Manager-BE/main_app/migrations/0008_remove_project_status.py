# Generated by Django 4.2.11 on 2024-03-14 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_rename_progress_project_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='status',
        ),
    ]