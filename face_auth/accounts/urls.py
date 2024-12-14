from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from .views import CustomLoginView, CustomRegisterView, CustomVerifyEmailView
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('registration/', CustomRegisterView.as_view(), name='custom_registration'),
    path('registration/account-confirm-email/<str:key>/', CustomVerifyEmailView.as_view(), name='account_confirm_email'),
    path('registration/password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('', include('dj_rest_auth.urls')),
]