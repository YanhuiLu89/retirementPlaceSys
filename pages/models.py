from django.db import models

# Create your models here.
class Users(models.Model):
    usertype = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    phone=models.CharField(max_length=50,default='')
    address=models.CharField(max_length=200,default='')

class Places(models.Model):
    name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=300,default='')
    introduce = models.TextField(max_length=2000)
    cost = models.IntegerField(default=3000)#费用
    traffic = models.CharField(max_length=100,default=u'高铁')#交通方式,高铁，航空，港口，可多选
    price = models.CharField(max_length=50,default=u'高')#物价，高，中，低  单选
    spotticket=models.CharField(max_length=50,default=u'贵')#景点门票，贵，较贵，便宜，较便宜 单选
    hospital=models.CharField(max_length=50,default=u'有三甲医院') #有三甲医院，无三甲医院，单选
    publishtime = models.DateTimeField('date published')

class Scenicspot(models.Model):
    place = models.ForeignKey(Places,on_delete=models.CASCADE)#place 是外键标志景点在哪个城市,多对一关系
    name = models.CharField(max_length=100)
    introduce = models.TextField(max_length=2000)
    address = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')
    opentime = models.CharField(max_length=100)

class Shares(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)#user 外键标志谁分享的
    place = models.ForeignKey(Places,on_delete=models.CASCADE)#place 外键,分享的是哪个地点
    text = models.CharField(max_length=500)#分享时写的内容
    time = models.DateTimeField('date published')#分享时间
