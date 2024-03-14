from django.shortcuts import render
from .models import Team, User, Project, Task
from .serializers import TeamSerializer, UserSerializer, ProjectSerializer, TaskSerializer
from rest_framework import mixins, generics, status, permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Create your views here.
class TeamCreateView(APIView):
    """create new team"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request, format=None):
        """get all teams a user belongs to"""
        serializer = TeamSerializer(request.user.teams.all(),
                                    many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """get data to create a new team"""
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            new_team = serializer.save()
            new_team.members.add(request.user)
            new_team.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(APIView):
    """create new user"""

    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request, format=None):
        """return current users"""
        serializer = UserSerializer(User.objects.all(), many=True)

        return Response(serializer.data)
    
    def post(self, request, format=None):
        """handle user creation"""
        serializer = UserSerializer(data=request.data)
        print(request.data, request.FILES)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(request.data.get('password'))
            new_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCreateView(APIView):
    """create new project"""

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """return current users projects"""
        teams = request.user.teams.all()
        projects = []
        for team in teams:
            projects.extend(team.projects.all())
        serializer = ProjectSerializer(projects, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """create a new project"""
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCreateView(APIView):
    """create new task"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """get all users tasks"""
        teams = request.user.teams.all()
        tasks = []
        for team in teams:
            projects = team.projects.all()
            for project in projects:
                tasks.extend(project.tasks.all())
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)
    
    def post(self, request, format=None):
        """create a new task"""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
