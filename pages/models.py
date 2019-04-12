from django.db import models

# Create your models here.
class Users(models.Model):
    usertype = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

class Places(models.Model):
    name = models.CharField(max_length=100)
    introduce = models.TextField(max_length=2000)
    address = models.CharField(max_length=300)
    time = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    publishtime = models.DateTimeField('date published')