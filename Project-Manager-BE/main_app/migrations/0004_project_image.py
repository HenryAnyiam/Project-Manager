# Generated by Django 4.2.11 on 2024-03-13 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_project_options_alter_task_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, upload_to='project_images'),
        ),
    ]
