from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validate_data):
        password = validate_data.pop('password', None)

        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class ProfileSerializer(serializers.Serializer):
    user  = UserSerializer(data=User)
    class Meta:
        model = Profile
        fields = ['user', 'profile_image', 'gender', 'description', 'university', 'course', 'year', 'collegeID']
