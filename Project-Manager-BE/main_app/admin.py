from django.contrib import admin
from .models import User, Team, Project, Task

# Register your models here.
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Task)
