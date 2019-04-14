from django.db import models

# Create your models here.
class Users(models.Model):
    usertype = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

class Places(models.Model):
    name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=300,default='')
    introduce = models.TextField(max_length=2000)
    cost = models.IntegerField(default=3000)#费用
    traffic_highrail = models.BooleanField(default=True)#交通方式
    traffic_air= models.BooleanField(default=False)
    traffic_port= models.BooleanField(default=False)
    price = models.IntegerField(default=0)#物价，0高，1中，2低
    spotticket=models.IntegerField(default=0)#景点门票，0贵，1较贵，2便宜，3较便宜
    hashospital=models.BooleanField(default=True)
    publishtime = models.DateTimeField('date published')

class Scenicspot(models.Model):
    place = models.ForeignKey(Places,on_delete=models.CASCADE)#place 是外键标志景点在哪个城市,多对一关系
    name = models.CharField(max_length=100)
    introduce = models.TextField(max_length=2000)
    address = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')
    opentime = models.CharField(max_length=100)
