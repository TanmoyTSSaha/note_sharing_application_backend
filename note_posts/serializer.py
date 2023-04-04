from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


# class PostLikeSerialzer(serializers.ModelSerializer):
#     class Meta:
#         model = Likes
#         fields = '__all__'