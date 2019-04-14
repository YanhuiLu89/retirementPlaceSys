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
    traffic = models.CharField(max_length=100,default=u'高铁')#交通方式,高铁，航空，港口，可多选
    price = models.CharField(max_length=50,default=u'高')#物价，高，中，低  单选
    spotticket=models.CharField(max_length=50,default=u'贵')#景点门票，贵，较贵，便宜，较便宜 单选
    hashospital=models.CharField(max_length=50,default=u'有三甲医院') #有三甲医院，无三甲医院，单选
    publishtime = models.DateTimeField('date published')

class Scenicspot(models.Model):
    place = models.ForeignKey(Places,on_delete=models.CASCADE)#place 是外键标志景点在哪个城市,多对一关系
    name = models.CharField(max_length=100)
    introduce = models.TextField(max_length=2000)
    address = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')
    opentime = models.CharField(max_length=100)
