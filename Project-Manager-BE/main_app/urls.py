from django.urls import path
from .auth import CustomAuthToken
from .views import TeamCreateView, UserCreateView, ProjectCreateView, TaskCreateView

urlpatterns = [
    path('api-auth', CustomAuthToken.as_view()),
    path('user', UserCreateView.as_view()),
    path('team', TeamCreateView.as_view()),
    path('project', ProjectCreateView.as_view()),
    path('task', TaskCreateView.as_view()),
]