from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "success",
            "data": serializer.data
        })
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializedProfile = ProfileSerializer(data=request.data)
        serializedProfile.is_valid(raise_exception=True)
        serializedProfile.save()
        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "success",
            "data": serializedProfile.data
        })

    def get(self, request):
        serializerProfile = ProfileSerializer(request.data)
        serializerUser = UserSerializer(request.data)
        return Response(serializerProfile.data + serializerUser.data)


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message":"User not found!",
                "data": {}
            })
        if not user.check_password(password):
            return Response({
                "status": status.HTTP_406_NOT_ACCEPTABLE,
                "message":"Incorrect password!",
                "data": {}
            })
        
        refresh = RefreshToken.for_user(user)        
        return Response({
            'status': status.HTTP_200_OK,
            'message':'success',
            'data': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        })