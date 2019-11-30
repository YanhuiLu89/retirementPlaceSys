from django.db import models

# Create your models here.
class Users(models.Model):
    usertype = models.IntegerField(default=0)#0-个人会员，1-管理员，2-养老机构
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    phone=models.CharField(max_length=50,default='')
    address=models.CharField(max_length=200,default='')

class Places(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE,null=True)#user 主键标志对应的会员账户，一对一关系
    name = models.CharField(max_length=100,default=u'未命名')
    phone=models.CharField(max_length=50,default='')#热线电话
    keywords = models.CharField(max_length=300,default='')
    introduce = models.TextField(max_length=2000,default='')
    cost = models.IntegerField(default=0)#费用
    traffic = models.CharField(max_length=100,default=u'高铁')#交通方式,高铁，航空，港口，可多选
    price = models.CharField(max_length=50,default=u'中')#物价，高，中，低  单选
    spotticket=models.CharField(max_length=50,default=u'贵')#景点门票，贵，较贵，便宜，较便宜 单选
    hospital=models.CharField(max_length=50,default=u'有三甲医院') #有三甲医院，无三甲医院，单选
    address = models.CharField(max_length=300)
    singleroomcount= models.IntegerField(default=20)#单人间个数
    singleroomfee= models.IntegerField(default=0)#单人间费用
    doubleroomcount= models.IntegerField(default=20)#双人间个数
    doubleroomfee= models.IntegerField(default=0)#双人间费用
    familyroomcount= models.IntegerField(default=20)#家庭间个数
    familyroomfee= models.IntegerField(default=0)#家庭间费用
    image = models.ImageField(upload_to='images',default="upimg/default.jpg") 
    likedcount=models.IntegerField(default=0)#点赞个数
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
    image = models.ImageField(upload_to='images',default='')

class Order(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)#user 主键标志下单者，一对一关系
    place = models.ForeignKey(Places,on_delete=models.CASCADE)#place 下单到哪个养老机构，一对一
    roomkind = models.CharField(max_length=100)#单人间，双人间，家庭间
    price= models.IntegerField(default=500)#价格
    guestname = models.TextField(max_length=50)#入住人名字
    phone=models.CharField(max_length=50,default='')#入住人电话
    guestnamecount= models.IntegerField(default=1)#入住人数
    checkintime = models.DateTimeField('date checkin')#入住时间

class Comment(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)#user 外键标志谁评论的
    place = models.ForeignKey(Places,on_delete=models.CASCADE)#place 外键评论的那个养老机构
    text = models.CharField(max_length=500)#评论的内容
    time = models.DateTimeField('date published')#评论时间
