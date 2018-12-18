from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


# class allUser(models.Model):
#     u_id = models.IntegerField(primary_key=True)
#     u_username = models.CharField(max_length=50,unique=True)
#     u_password = models.CharField(max_length=100)
#     u_email = models.EmailField(max_length=50,default='1176378069@qq.com')
#     u_isactive = models.BooleanField(default=False)
#     u_head = models.FilePathField(default='uploads/default.jpg')
#     u_isdelete = models.BooleanField(default=False)

class User(AbstractUser):
    userhead = models.ImageField(default='uploads/default.jpg',upload_to='uploads/icon')
    is_delete = models.BooleanField(default=False)
    is_sensitize = models.BooleanField(default=False)

class Data_yunpan(models.Model):
    id= models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    href = models.CharField(max_length=100)
    downurl = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    img_url = models.CharField(max_length=200)



