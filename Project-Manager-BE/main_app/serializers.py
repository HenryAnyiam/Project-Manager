from rest_framework import serializers
from .models import User, Team, Project, Task


class TeamSerializer(serializers.ModelSerializer):
    """handle team serialization and deserialization"""

    class Meta:
        model = Team
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    """handle user serialization and deserialization"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_pic', 'teams']


class ProjectSerializer(serializers.ModelSerializer):
    """handle project serialization and deserialization"""
    due_in = serializers.CharField(read_only=True)
    done_tasks = serializers.CharField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    """handle task serialization and deserialization"""

    class Meta:
        model = Task
        fields = "__all__"