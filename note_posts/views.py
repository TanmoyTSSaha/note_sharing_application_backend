from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Like
from .serializer import PostSerializer, PostLikeSerializer

# Create your views here.

class PostListView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request):
        postSerializer = PostSerializer(data=request.data)
        
        if postSerializer.is_valid():
            try:
                postSerializer.save()    
            except Exception as e:
                return Response({'error':'Unable to create post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(
                {
                    'status':status.HTTP_201_CREATED,
                    'message': 'SUCCESS'
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({'error':'Unable to create post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        posts = Post.objects.all()[:20]
        postSerializer = PostSerializer(posts, many=True)
        return Response({'status':status.HTTP_200_OK, 'message':'OK','data':postSerializer.data}, status=status.HTTP_200_OK)
    
    def get(self, request, user_id):
        posts = Post.objects.get(user_id=user_id)
        postSerializer = PostSerializer(posts, many=True)
        return Response({'status':status.HTTP_200_OK, 'message':'OK','data':postSerializer.data}, status=status.HTTP_200_OK)


class PostDetailedView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self, post_id):
        try:
            return Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, post_id):
        post = self.get_object(post_id=post_id)
        postSerializer=PostSerializer(post)
        return Response(postSerializer.data)
    
    def put(self, request, post_id):
        post = self.get_object(post_id=post_id)
        if request.user != post.post_author:
            return Response({'status':status.HTTP_403_FORBIDDEN, 'message':'Request denied'}, status=status.HTTP_403_FORBIDDEN)
        postSerializer = PostSerializer(post, data=request.data)
        if postSerializer.is_valid():
            postSerializer.save()
            return Response(postSerializer.data)
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':postSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = self.get_object(post_id=post_id)
        if request.user != post.post_author:
            return Response({'status':status.HTTP_403_FORBIDDEN, 'message':'Request denied'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'DELETED'}, status=status.HTTP_204_NO_CONTENT)
    

class PostLikeAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        user = request.user
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'You have already liked the post.'}, status=status.HTTP_400_BAD_REQUEST)
        likeSerializer = PostLikeSerializer(like)
        return Response({'status':status.HTTP_201_CREATED, 'data':likeSerializer.data}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        user = request.user
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_like_count(self, post):
        return Like.objects.filter(post=post).count()
    
    def get(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        like_count = self.get_like_count(post)
        return Response({'status':status.HTTP_200_OK, 'like_count':like_count}, status=status.HTTP_200_OK)
    
class CommentAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, post_id):
        pass