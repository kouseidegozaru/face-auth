from rest_framework.views import APIView
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from .serializers import CustomLoginSerializer, CustomRegisterSerializer
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        # メールが既に送信済の場合
        if get_user_model().objects.filter(email=serializer.validated_data['email']).exists():
            return Response(
                {'detail': 'User already exists'},
                status=status.HTTP_409_CONFLICT,
                headers=headers,
            )
        
        user = self.perform_create(serializer)
        data = self.get_response_data(user)

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response

class CustomVerifyEmailView(VerifyEmailView):
    
    def get(self, request, *args, **kwargs):
        # デバッグ時のみgetリクエストを許可
        if settings.DEBUG:
            return self.post(request, *args, **kwargs)
        else:
            raise MethodNotAllowed('GET')

class CsrfTokenView(APIView):
    def get(self, request, *args, **kwargs):
        # CSRFトークンを発行してJSON形式で返す
        return JsonResponse({'csrfToken': get_token(request)})
