from django.urls import path

from .views import PostListView, PostDetailedView

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('post=<int:post_id>/', PostDetailedView.as_view(), name='post_detail'),
    path('user=<int:user_id>/', PostListView.as_view(), name='user_posts')
]