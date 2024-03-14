from rest_framework import serializers
from .models import User, Team, Project, Task


class TeamSerializer(serializers.ModelSerializer):
    """handle team serialization and deserialization"""
    users = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=User.objects.all(),
                                               required=False,
                                               allow_null=True)
    projects = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Project.objects.all(),
                                                  required=False,
                                                  allow_null=True)

    class Meta:
        model = Team
        fields = ["id", "name", "users", "projects"]

class UserSerializer(serializers.ModelSerializer):
    """handle user serialization and deserialization"""
    teams = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Team.objects.all(),
                                               required=False,
                                               allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_pic', 'teams']


class ProjectSerializer(serializers.ModelSerializer):
    """handle project serialization and deserialization"""
    tasks = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Task.objects.all(),
                                               required=False,
                                               allow_null=True)
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