from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import logout
# from rest_framework.renderers import JSONRenderer

from .serializers import UserSerializer, ProfileSerializer
from .models import User


class UserRegister(APIView):
    permission_classes=[permissions.AllowAny]
    # renderer_classes=[JSONRenderer]
    
    def post(self, request):
        userSerializer = UserSerializer(data=request.data)

        if userSerializer.is_valid():
            try:
                user = userSerializer.save()

            except Exception as e:
                return Response({'error': 'Unable to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user:
                refreshToken = RefreshToken.for_user(user)
                response = {
                    'refresh':str(refreshToken),
                    'access':str(refreshToken.access_token)
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else: return Response({'error': 'Unable to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]
    # renderer_classes=[JSONRenderer]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            refreshToken = RefreshToken.for_user(user)
            response = {
                'refresh':str(refreshToken),
                'access':str(refreshToken.access_token)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserLogoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    # renderer_classes=[JSONRenderer]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'user logged out successfully'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message': 'something wnet wrong try again'},status=status.HTTP_400_BAD_REQUEST)


    
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes=[JSONRenderer]

    def get(self, request):
        userSerializer = UserSerializer(request.user)
        return Response(userSerializer.data)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes=[JSONRenderer]

    def get(self, request):
        userProfileSerialized = ProfileSerializer(request.user.profile)
        return Response(userProfileSerialized.data)

    def post(self, request):
        serializedProfile = ProfileSerializer(data=request.data)
        if serializedProfile.is_valid():
            serializedProfile.save()
            return Response(serializedProfile.data, status=status.HTTP_200_OK)
        return Response(serializedProfile.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_profile = request.data.profile
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)