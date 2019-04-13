from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils import timezone

from .models import Users,Places
import time

# Create your views here.
def index(request):#入口页
    if request.method == 'POST':  
        temp_name = request.POST['username']
        temp_psw = request.POST['password']
        temp_mail = request.POST['mail']
        print( temp_name+","+temp_psw+","+temp_mail)
        if Users.objects.filter(name=temp_name).exists():
            messages.add_message(request,messages.ERROR,'该用户名已经存在')
            return render(request,'pages/index.html')
        if Users.objects.filter(email=temp_mail).exists():
            messages.add_message(request,messages.ERROR,'该邮箱已经注册过')
            return render(request,'pages/index.html')
        user = Users(usertype=0,name=temp_name, password=temp_psw, email=temp_mail)
        user.save()
        messages.add_message(request,messages.INFO,'注册成功')
        return render(request,'pages/index.html')
    return render(request,'pages/index.html')

def logout(request):#退出
    return render(request,'pages/index.html')

def login(request):#登陆
    if request.method == 'POST':
        name = request.POST['username']
        password =  request.POST['password']
        usertype=int((request.POST['usertype']))
        # 查询用户是否在数据库中
        print("%s,%s,%d"%(name,password,usertype))
        if Users.objects.filter(name=name).exists():
            print("111111111111111111111")
            user=Users.objects.get(name=name)
            print("%s,%s,%d" % (user.name,user.password,user.usertype))
            print(user.password+",%d" % user.usertype)
            if user.password==password and user.usertype==usertype:
                print("2222222222222222222")
                if user.usertype==1:
                    return render(request, 'pages/homepage_a.html',placelist())#跳到管理员首页界面
                else:
                    return render(request, 'pages/homepage.html',placelist())#跳到会员首页界面
            else:
                messages.add_message(request,messages.ERROR,'用户密码或身份类型错误错误')
                return render(request, 'pages/login.html')
        else:
            print("333333333333333333333")
            messages.add_message(request,messages.ERROR,'用户不存在')
            return render(request, 'pages/login.html')
    return render(request, 'pages/login.html')

def placelist():#地址列表
    place_list = Places.objects.all()
    context = {'place_list': place_list}
    return context

def addspot(request):#添加景点界面
    return render(request, 'pages/admin_addplace.html')

def home(request):#去首页
    return render(request, 'pages/homepage.html')

def myinfo(request):#我的界面
    return render(request, 'pages/homepage.html')

def addplace(request):#添加地点页面
    if request.method == 'POST':
        name = request.POST['name']
        introduce = request.POST['introduce']
        price= int(request.POST['price'])

        if name!="":
            place=Places(name=name,introduce=introduce,price=price,publishtime=timezone.now())
            place.save()
            messages.add_message(request,messages.INFO,'添加成功')
            return render(request, 'pages/admin_addplace.html')
        else:
            messages.add_message(request,messages.INFO,'名称不能为空')
            return render(request, 'pages/admin_addplace.html')
        return render(request, 'pages/admin_addplace.html')
    return render(request,'pages/admin_addplace.html')