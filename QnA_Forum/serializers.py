from rest_framework import serializers
from .models import QnaModel, QnaCommentModel

class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaModel
        fields = '__all__'

class QnaCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaCommentModel
        fields = '__all__'

