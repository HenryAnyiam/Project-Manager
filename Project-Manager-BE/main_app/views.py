from django.shortcuts import render
from .models import Team, User, Project, Task
from .serializers import TeamSerializer, UserSerializer, ProjectSerializer, TaskSerializer
from rest_framework import status, permissions
from django.http import Http404
from django.core.exceptions import ValidationError
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

class TeamDetailView(APIView):
    """Retrieve, update or delete a team instance"""

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_object(self, pk):
        """get team object"""

        try:
            return Team.objects.get(id=pk)
        except Team.DoesNotExist:
            raise Http404
        except ValidationError:
            raise Http404
    
    def get(self, request, pk, format=None):
        """retieve team data"""
        team = self.get_object(pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """update team data"""
        team = self.get_object(pk)
        if request.user in team.members.all():
            if 'projects' in request.data:
                del request.data['projects']
            if 'users' in request.data:
                del request.data['users']
            serializer = TeamSerializer(team, data=request.data, partial=True)
            if serializer.is_valid():
                team = serializer.save()
                if 'user' in request.data:
                    try:
                        user = User.objects.get(request.data.get('user'))
                    except User.DoesNotExist:
                        raise Http404
                    else:
                        team.members.add(user)
                        team.save()
                if 'projects' in request.data:
                    try:
                        project = Project.objects.get(request.data.get('project'))
                    except Project.DoesNotExist:
                        raise Http404
                    else:
                        team.projects.add(project)
                        team.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format=None):
        """delete team data"""
        team = self.get_object(pk)
        if request.user in team.users.all():
            team.users.remove(request.user)
            team.save()
            if len(team.users.all()) == 0:
                team.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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
        if serializer.is_valid():
            if 'password' not in request.data:
                return Response({'password': "This field is required"},
                                status=status.HTTP_400_BAD_REQUEST)
            new_user = serializer.save()
            new_user.set_password(request.data.get('password'))
            new_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetailView(APIView):
    """retrieve, update and delete a user instance"""

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_object(self, pk):
        """get user instance"""
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
        except ValidationError:
            raise Http404
    
    def get(self, request, pk=None, format=None):
        """get a user"""
        if pk:
            serializer = UserSerializer(self.get_object(pk))
        else:
            serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        """update a user details"""
        if pk and pk != str(request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if 'password' in request.data:
            request.user.set_password(request.data.get('password'))
            request.user.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        """delete user details"""
        if pk and pk != str(request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = self.get_object(request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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


class ProjectDetailView(APIView):
    """retrieve, update or delete a project instance"""

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_object(self, pk):
        """get a project instance"""
        try:
            return Project.objects.get(id=pk)
        except Project.DoesNotExist:
            raise Http404
        except ValidationError:
            raise Http404
    
    def get(self, request, pk, format=None):
        """get project details"""
        serializer = ProjectSerializer(self.get_object(pk))

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """update project details"""
        project = self.get_object(pk)
        if "team" in request.data:
            del request.data['team']
        if request.user in project.team.members.all():
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format=None):
        """delete a project"""
        project = self.get_object(pk)
        if request.user in project.team.members.all():
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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


class TaskDetailView(APIView):
    """retirve, update and delete a task"""

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        """get task instance"""
        try:
            return Task.objects.get(id=pk)
        except Task.DoesNotExist:
            raise Http404
        except ValidationError:
            raise Http404
    
    def get(self, request, pk, format=None):
        """get task details"""
        serializer = TaskSerializer(self.get_object(pk))

        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """update a task instance"""
        task = self.get_object(pk)
        if request.user in task.project.team.members.all():
            if 'project' in request.data:
                del request.data['project']
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format=None):
        """delete a task instance"""
        task = self.get_object(pk)
        if request.user in task.project.team.members.all():
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
