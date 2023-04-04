from django.db import models
from django.urls import reverse
from user.models import User


# Create your models here.
class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    post_content = models.TextField(null=True, max_length=5000)
    post_image = models.ImageField(null=True, upload_to='note_picture')
    post_file = models.FileField(null=True, upload_to='note_file')
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_liked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.post_content[:20]
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
# class Likes(models.Model):
#     user_id = models.ManyToManyField(User, null=False)
#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
#     total_likes = models.IntegerField(default=0)
    