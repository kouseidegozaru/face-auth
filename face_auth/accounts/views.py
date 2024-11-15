from django.http import HttpResponseRedirect
from django.conf import settings
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from .serializers import CustomLoginSerializer, CustomRegisterSerializer
from rest_framework.exceptions import MethodNotAllowed


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class CustomVerifyEmailView(VerifyEmailView):
    
    def get(self, request, *args, **kwargs):
        # デバッグ時のみgetリクエストを許可
        if settings.DEBUG:
            return self.post(request, *args, **kwargs)
        else:
            raise MethodNotAllowed('GET')
