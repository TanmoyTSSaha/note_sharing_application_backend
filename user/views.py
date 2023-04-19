from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.renderers import JSONRenderer

from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile


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
        return Response({'status':status.HTTP_401_UNAUTHORIZED, 'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserLogoutView(APIView):
    permission_classes=[JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({'status':status.HTTP_205_RESET_CONTENT, 'message': 'user logged out successfully'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message': 'something wnet wrong try again'},status=status.HTTP_400_BAD_REQUEST)

    
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes=[JSONRenderer]

    def get(self, request):
        userSerializer = UserSerializer(request.user)
        return Response({'status':status.HTTP_200_OK, 'message':'OK','data':userSerializer.data,}, status=status.HTTP_200_OK)
    
class SingleUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except Exception as e:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = self.get_user(id=id)
        userSerializer = UserSerializer(user)
        return Response({'status':status.HTTP_200_OK, 'message':'OK','data':userSerializer.data,}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes=[JSONRenderer]

    def get_object(self):
        return self.request.user.profile
    
    def put(self, request, *args, **kwargs):
        profileSerializer = ProfileSerializer(instance=self.get_object(), data=request.data)
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({'status':status.HTTP_200_OK, 'message':'OK', 'data':profileSerializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        userProfileSerialized = ProfileSerializer(request.user.profile)
        return Response({'status':status.HTTP_200_OK, 'message':'OK', 'data':userProfileSerialized.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializedProfile = ProfileSerializer(data=request.data)
        if serializedProfile.is_valid():
            serializedProfile.save()
            return Response(serializedProfile.data, status=status.HTTP_200_OK)
        return Response(serializedProfile.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_profile = request.data.profile
        user_profile.delete()
        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'DELETED'}, status=status.HTTP_204_NO_CONTENT)
    
class SingleUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_profile(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        

    def get(self, request, user):
        profile = self.get_profile(user=user)
        userProfileSerialized = ProfileSerializer(profile)
        return Response({'status':status.HTTP_200_OK, 'message':'OK', 'data':userProfileSerialized.data}, status=status.HTTP_200_OK)