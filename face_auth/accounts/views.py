from django.http import HttpResponseRedirect
from django.conf import settings
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from .serializers import CustomLoginSerializer, CustomRegisterSerializer

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class CustomVerifyEmailView(VerifyEmailView):
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        
        # メール認証後のリダイレクト先URLを取得
        redirect_url = settings.VERIFY_EMAIL_REDIRECT_URL
        return HttpResponseRedirect(redirect_url)
