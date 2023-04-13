from django.urls import path
from .views import QnaAPIView, QnaDetailedAPIView, QnaCommentAPIView, QnaCommentGetAPIView, QnaCommentPutDeleteAPIView

urlpatterns = [
    path('', QnaAPIView.as_view(), name='post-get-qna'),
    path('qna=<int:qna_id>/', QnaDetailedAPIView.as_view(), name='get-put-delete-qna'),
    path('new_comment/', QnaCommentAPIView.as_view(), name='post-qna-comment'),
    path('new_comment/qna=<int:qna_id>', QnaCommentGetAPIView.as_view(), name='get-qna-comment'),
    path('new_comment/qna_comment=<int:qna_comment_id>', QnaCommentPutDeleteAPIView.as_view(), name='put-delete-qna-comment')
]