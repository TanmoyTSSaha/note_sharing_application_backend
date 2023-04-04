from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializer import PostSerializer

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
        return Response(postSerializer.data)
    

class PostDetailedView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self, post_id):
        try:
            return Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, post_id):
        post = self.get_object(post_id=post_id)
        postSerializer=PostSerializer(self)
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
    



# class PostLikeView(APIView):
#     permission_classes=[permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.data.get('user_id')
#         post = Post.objects.filter(post_id=request.data.get('post_id'))
#         current_likes = post.post_liked
#         post_liked = Likes.objects.filter(user=user, post=post).count()

#         if not post_liked:
#             post_liked = Likes.objects.create(user=user, post=post)
#             current_likes = current_likes + 1
#         else:
#             post_liked = Likes.objects.filter(user=user, post=post).delete()
#             current_likes = current_likes - 1

#         return Response(
#             {
#                 'status':status.HTTP_200_OK,
#                 'message': 'OK',
#                 'current_likes': current_likes
#             },
#             status=status.HTTP_200_OK
#         )
