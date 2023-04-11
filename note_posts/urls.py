from django.urls import path

from .views import PostListView, PostDetailedView, PostLikeAPIView, CommentAPIView, UserPostAPIView, CommentGetAPIView, CommentPutDeleteAPIView

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('post=<int:post_id>/', PostDetailedView.as_view(), name='post_detail'),
    path('user=<int:user_id>/', UserPostAPIView.as_view(), name='user_posts'),
    path('post=<int:post_id>/like/', PostLikeAPIView.as_view(), name='post-like'),
    path('comment/create/', CommentAPIView.as_view(), name='comment-POST'),
    path('comment/post=<int:post_id>/', CommentGetAPIView.as_view(), name='comment-GET'),
    path('comment/delete=<int:comment_id>/', CommentPutDeleteAPIView.as_view(), name='comment-DELETE'),
    path('comment/update=<int:comment_id>/', CommentPutDeleteAPIView.as_view(), name='comment-UPDATE'),
]
