from django.urls import path, include
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls'))
]