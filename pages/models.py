from django.db import models

# Create your models here.
class Users(models.Model):
    usertype = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

class Places(models.Model):
    name = models.CharField(max_length=50)
    introduce = models.CharField(max_length=300)
    address = models.CharField(max_length=50)
    time = models.DateTimeField(max_length=50)
    image=models.CharField(max_length=50)