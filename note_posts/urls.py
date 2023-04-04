from django.urls import path

from .views import PostListView, PostDetailedView

urlpatterns = [
    path('post/', PostListView.as_view(), name='posts'),
    path('post/post_details', PostDetailedView.as_view(), name='post_detail')
]