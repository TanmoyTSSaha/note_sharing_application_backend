from django.urls import path

from .views import PostListView, PostDetailedView, PostLikeAPIView

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('post=<int:post_id>/', PostDetailedView.as_view(), name='post_detail'),
    path('user=<int:user_id>/', PostListView.as_view(), name='user_posts'),
    path('post=<int:post_id>/like', PostLikeAPIView.as_view(), name='post-like')
]
