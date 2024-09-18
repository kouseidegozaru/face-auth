from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.registration.views import get_adapter
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }

    def save(self, request):
        
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()
        
        # ユーザー情報をシリアライザーから取得
        email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password1')
        
        # ユーザーの作成
        user = User.objects.create_user(email=email, name=name, password=password)
        
        # ユーザーの保存
        adapter.save_user(request, user, self)
        
        return user

class CustomLoginSerializer(LoginSerializer):

    username = None