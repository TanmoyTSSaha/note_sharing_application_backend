from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserRegister, UserLogin, UserProfileView, UserView, UserLogoutView, SingleUserProfileView, SingleUserView


urlpatterns = [
    path('api/register/', UserRegister.as_view(), name='register'),
    path('api/login/', UserLogin.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', UserLogoutView.as_view(), name='logout'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/profile/user=<int:user>', SingleUserProfileView.as_view(), name='single_user_profile'),
    path('api/user/', UserView.as_view(), name='user'),
    path('api/user/user=<int:id>', SingleUserView.as_view(), name='single_user'),
]