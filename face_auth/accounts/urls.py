from django.urls import path, include
from .views import CustomLoginView, CustomRegisterView
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('registration/', CustomRegisterView.as_view(), name='custom_registration'),
    path('', include('dj_rest_auth.urls')),
]