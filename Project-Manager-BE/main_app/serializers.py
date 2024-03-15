from rest_framework import serializers
from .models import User, Team, Project, Task


class TeamSerializer(serializers.ModelSerializer):
    """handle team serialization and deserialization"""
    members = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=User.objects.all(),
                                               required=False,
                                               allow_null=True)
    projects = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Project.objects.all(),
                                                  required=False,
                                                  allow_null=True)

    class Meta:
        model = Team
        fields = ["id", "name", "members", "projects"]
    

class UserSerializer(serializers.ModelSerializer):
    """handle user serialization and deserialization"""
    teams = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Team.objects.all(),
                                               required=False,
                                               allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_pic', 'teams']
    

    def update(self, instance, validated_data):
        """update team instance"""
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'profile_pic' in validated_data:
            instance.clear_older_images()
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    """handle project serialization and deserialization"""
    tasks = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Task.objects.all(),
                                               required=False,
                                               allow_null=True)
    due_in = serializers.CharField(read_only=True)
    done_tasks = serializers.CharField(read_only=True)
    status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
    
    def update(self, instance, validated_data):
        """update team instance"""
        instance.name = validated_data.get('name', instance.name)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.due_time = validated_data.get('due_time', instance.due_time)
        if 'image' in validated_data:
            instance.clear_older_images()
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    """handle task serialization and deserialization"""

    class Meta:
        model = Task
        fields = "__all__"
    