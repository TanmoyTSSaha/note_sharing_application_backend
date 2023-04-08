import os
from PIL import Image
from pathlib import Path
from django.db import models
from django.contrib.auth.models import AbstractUser

BASE_DIR = Path(__file__).resolve().parent.parent


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    name= models.CharField(max_length=100)
    email = models.EmailField(max_length=300, unique=True, null=False)
    password = models.CharField(max_length=200, null=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = self.first_name + ' ' + self.last_name
        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_picture', blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=500, blank=True)
    university = models.CharField(max_length=200, blank=True)
    course = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(blank=True)
    collegeID = models.ImageField(upload_to='college_id', null=True, blank=True)

    def __str__(self):
        return self.user.username + ' Profile'
    
