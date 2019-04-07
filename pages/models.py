from django.db import models

# Create your models here.
class User(models.Model):
    usertype = models.IntegerField(default=0)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField()