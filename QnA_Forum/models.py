from django.db import models
from user.models import User

# Create your models here.
class QnaModel(models.Model):
    qna_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=500, null=False, blank=False)
    question_description = models.TextField(null=False, blank=False)
    question_image = models.ImageField(null=True, blank=True, upload_to='QnA_Forum')

    def __str__(self):
        return self.question_title
    

class QnaCommentModel(models.Model):
    qna_comment_id = models.AutoField(primary_key=True)
    qna_id = models.ForeignKey(QnaModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField(null=False, blank=False)
    comment_image = models.ImageField(null=True, blank=True, upload_to='Qna_comment_image')