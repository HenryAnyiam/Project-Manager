from django.contrib.auth.backends import ModelBackend
from main_app.models import User

class CustomUserAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None