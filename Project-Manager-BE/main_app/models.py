from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from os import path, remove
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Team(models.Model):
    """model to map to Team table"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)

class User(AbstractUser):
    """model to map to User table"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    confirmed_email = models.BooleanField(default=False)
    teams = models.ManyToManyField(Team, related_name="members")

    def __str__(self) -> str:
        return f'User: {self.email} {self.username}'

    def clear_older_images(self):
        """clear older images before setting a new one"""
        if self.profile_pic and path.isfile(self.profile_pic.path):
            remove(self.profile_pic.path)


    def confirm_email(self):
        """confirm user email"""
        self.confirmed_email = True
        self.save()


class Project(models.Model):
    """map to Project table"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="projects")
    due_date = models.DateField()
    due_time = models.TimeField()
    image = models.ImageField(upload_to="project_images", blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    progress = models.IntegerField(default=0)

    def clear_older_images(self):
        """clear older images before setting a new one"""
        if self.image and path.isfile(self.image.path):
            remove(self.image.path)

    @property
    def due_in(self):
        """assign due_in field"""
        project_date = datetime.combine(self.due_date, self.due_time)
        due_date = project_date - datetime.now()
        if due_date.days < 0 or due_date.seconds < 0:
            return "Overdue"
        return f"{due_date.days}d, {due_date.seconds // 60}m"
    
    @property
    def done_tasks(self):
        """get total tasks"""

        return f"{len(self.tasks.filter(done=True))} / {len(self.tasks.all())}" 
    
    def update_progress(self):
        """update project progress"""
        all_tasks = self.tasks.all()
        done_tasks = self.tasks.filter(done=True)
        self.progress = (len(done_tasks) / len(all_tasks)) * 100
        self.save()
    
    def __str__(self):
        return f"Project: {self.name}"
    
    class Meta:
        ordering = ["created_at"]


class Task(models.Model):
    """map to Task table"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Task: {self.name}"
    
    class Meta:
        ordering = ["created_at"]