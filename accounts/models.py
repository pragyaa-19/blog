from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class  MyUser(AbstractUser):
    email = models.EmailField(blank=True,null=True)
    fullname = models.CharField(max_length=50,default="user")
    bio = models.CharField(max_length=250,default="")
    
    def __str__(self):
        return self.username