from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QnaSerializer, QnaCommentSerializer
from .models import QnaModel, QnaCommentModel


class QnaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        qnaSerializer = QnaSerializer(data=request.data)
        if qnaSerializer.is_valid():
            try:
                qnaSerializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'message':'CREATED'},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'BAD REQUEST'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            qna = QnaModel.objects.all()
            qnaSerializer = QnaSerializer(qna, many=True)
            return Response({'status':status.HTTP_200_OK, 'message':'OK', 'data':qnaSerializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QnaDetailedAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, qna_id):
        try:
            qna = QnaModel.objects.get(qna_id=qna_id)
            qnaSerializer = QnaSerializer(qna)
            return Response({'status':status.HTTP_200_OK, 'message':'OK', 'data':qnaSerializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, qna_id):
        qna = QnaModel.objects.get(qna_id=qna_id)
        if request.user != qna.user:
            return Response({'status':status.HTTP_403_FORBIDDEN, 'message':'REQUEST DENIED'}, status=status.HTTP_403_FORBIDDEN)
        qnaSerializer = QnaSerializer(qna, data=request.data)
        if qnaSerializer.is_valid():
            qnaSerializer.save()
            return Response({'status':status.HTTP_202_ACCEPTED,'message':'UPDATED','data':qnaSerializer.data},status=status.HTTP_202_ACCEPTED)
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'BAD REQUEST', 'data':qnaSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, qna_id):
        qna = QnaModel.objects.get(qna_id=qna_id)
        if request.user != qna.user:
            return Response({'status':status.HTTP_403_FORBIDDEN, 'message':'REQUEST DENIED'}, status=status.HTTP_403_FORBIDDEN)
        qna.delete()
        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'DELETED'}, status=status.HTTP_204_NO_CONTENT)

class QnaCommentAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request):
        qnaCommentSerializer = QnaCommentSerializer(data=request.data)
        if qnaCommentSerializer.is_valid():
            try:
                qnaCommentSerializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'message':'CREATED'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message':f'{e}'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'BAD REQUEST'},status=status.HTTP_400_BAD_REQUEST)
        
class QnaCommentGetAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, qna_id):
        try:
            qnaComments = QnaCommentModel.objects.filter(qna_id=qna_id)
            qnaCommentSerializer = QnaCommentSerializer(qnaComments, many=True)
            return Response({'status':status.HTTP_200_OK, 'message':'OK', 'data':qnaCommentSerializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class QnaCommentPutDeleteAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def put(self, request, qna_comment_id):
        qnaComment = QnaCommentModel.objects.get(qna_comment_id=qna_comment_id)

        if request.user != qnaComment.user:
            return Response({'status':status.HTTP_403_FORBIDDEN, 'message':'REQUEST DENIED'}, status=status.HTTP_403_FORBIDDEN)
        else:
            qnaCommentSerializer = QnaCommentSerializer(data=request.data)
            if qnaCommentSerializer.is_valid():
                qnaCommentSerializer.save()
                return Response({'status':status.HTTP_202_ACCEPTED, 'message':'UPDATED', 'data':qnaCommentSerializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'BAD REQUEST', 'data':qnaCommentSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, qna_comment_id):
        qnaComment = QnaCommentModel.objects.get(qna_comment_id=qna_comment_id)
        if request.user != qnaComment.user:
            return Response({'status':status.HTTP_403_FORBIDDEN, 'message':'REQUEST DENIED'}, status=status.HTTP_403_FORBIDDEN)
        else:
            qnaComment.delete()
            return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'DELETED'}, status=status.HTTP_204_NO_CONTENT)