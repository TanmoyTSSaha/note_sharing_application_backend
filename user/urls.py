from django.urls import path
from .views import Register, Login, ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', Register.as_view(), name='sign_up'),
    path('login/', Login.as_view(), name='sign_in'),
    path('user_profile/', ProfileView.as_view(), name='user_profile')
]