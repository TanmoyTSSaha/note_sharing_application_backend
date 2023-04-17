from django.db import models
from django.urls import reverse
from user.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    post_content = models.TextField(null=False, blank=False, max_length=5000)
    post_image = models.ImageField(null=True, blank=True, upload_to='note_picture')
    post_file = models.FileField(null=True, blank=True, upload_to='note_file')
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_liked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.post_id) + '. ' + self.post_content[:20] + '...'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} likes {self.post.post_content[:20]}...'
    
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_content = models.TextField(max_length=1000, null=False, blank=False)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} commented {self.post.post_content[:20]}...'