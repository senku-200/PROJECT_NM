from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    firstname = models.CharField(max_length=100,null = True,blank=True)
    lastname = models.CharField(max_length=100,null = True,blank=True)
    profile_image = models.ImageField(upload_to='D:\PROJECT NM\Scripts\project\static\data',null = True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username

class Project(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    template = models.ImageField(upload_to='D:\PROJECT NM\Scripts\project\static\data',null = True,blank=True)
    discription = models.TextField()
    likes = models.ManyToManyField(User,related_name="prj_likes")
    dislikes = models.ManyToManyField(User,related_name="prj_dislikes")
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    comment = models.TextField(null=True,blank=True)
    likes = models.ManyToManyField(User,related_name="cmt_likes")
    dislikes = models.ManyToManyField(User,related_name="cmt_dislikes")
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:50]


class ObjectDetector(models.Model):
    image = models.ImageField(upload_to='D:\PROJECT NM\Scripts\project\data',null = True,blank=True)
