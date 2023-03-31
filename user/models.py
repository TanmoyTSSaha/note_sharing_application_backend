from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    first_name = models.CharField(max_length=300, null=False)
    last_name = models.CharField(max_length=300, null=False)
    name= str(first_name) + str(last_name)
    email = models.EmailField(max_length=300, unique=True, null=False)
    password = models.CharField(max_length=200, null=False)
    username = models.CharField(max_length=300, unique=True, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'password']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default= 'media/profile_picture/profile_avatar_m.png', upload_to='media/profile_picture')
    gender = models.CharField(max_length=10)
    description = models.CharField(max_length=500)
    university = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    year = models.IntegerField()
    collegeID = models.ImageField(default= 'media/college_id/defult_college_id.jpg', upload_to='media/college_id', null=True)

    def __str__(self):
        return self.user.username + ' Profile'
    
    def post(self, *args, **kwargs):
        self.update(*args, **kwargs)

        profileImg = Image.open(self.profile_image.path)
        collegeIDImg = Image.open(self.collegeID.path)
        
        if profileImg.height > 1000 or profileImg.width > 1000:
            output_size = (1000,1000)
            profileImg.thumbnail(output_size)
            profileImg.save(self.profile_image.path)

        if collegeIDImg.height > 500 or collegeIDImg.width > 500:
            output_size = (500,500)
            collegeIDImg.thumbnail(output_size)
            collegeIDImg.save(self.collegeID.path)
