from django.urls import path
from .auth import CustomAuthToken
from .views import TeamCreateView, UserCreateView, ProjectCreateView, TaskCreateView
from .views import TeamDetailView, UserDetailView, ProjectDetailView, TaskDetailView

urlpatterns = [
    path('api-auth', CustomAuthToken.as_view()),
    path('user', UserCreateView.as_view()),
    path('team', TeamCreateView.as_view()),
    path('project', ProjectCreateView.as_view()),
    path('task', TaskCreateView.as_view()),
    path('task-detail/<pk>', TaskDetailView.as_view()),
    path('user-detail', UserDetailView.as_view()),
    path('user-detail/<pk>', UserDetailView.as_view()),
    path('project-detail/<pk>', ProjectDetailView.as_view()),
    path('team-detail/<pk>', TeamDetailView.as_view()),
]