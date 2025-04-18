from django.urls import path
from .views import UserCreateAPIView, CustomAuthToken, UserProfileView

urlpatterns = [
    path('users/', UserCreateAPIView.as_view(), name='user-create'),
    path('auth/token/', CustomAuthToken.as_view(), name='auth-token'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
]