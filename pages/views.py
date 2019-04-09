from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.files.base import ContentFile

from .models import Users,Places
import time

# Create your views here.
def index(request):#index,首页
    if request.method == 'POST':     
        if 'regist' in request.POST:
            return render(request, 'pages/regist.html')#跳转到注册页面    
        elif  'login' in request.POST: 
            return render(request, 'pages/login.html')#跳转到登陆页面        
    return render(request, 'pages/index.html')

def regist(request):#注册
    if request.method == 'POST':  
        temp_name = request.POST['username']
        temp_psw = request.POST['password']
        temp_mail = request.POST['mail']
        print( temp_name+","+temp_psw+","+temp_mail)
        if Users.objects.filter(name=temp_name).exists():
            return HttpResponse("该用户名已经存在！！！")
        if Users.objects.filter(email=temp_mail).exists():
            return HttpResponse("该邮箱已经注册过！！！")
        user = Users(usertype=0,name=temp_name, password=temp_psw, email=temp_mail)
        user.save()
        return HttpResponse("注册成功")

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
                    return render(request, 'pages/placelist_add.html')
                else:
                    return render(request, 'pages/placelist.html')
            else:
                # return HttpResponse('用户密码错误')
                return render(request, 'pages/login.html', {'password': '用户密码或身份类型错误错误'})
        else:
            # return HttpResponse('用户不存在')
            return render(request, 'pages/login.html', {'name': '用户不存在'})

def placelist(request):#地址列表
    place_list = Places.objects.all()
    context = {'place_list': place_list}
    return render(request, 'lib/placelist.html', context)

def toadd(request):#添加
    return render(request, 'lib/placelist_add.html')

def toview(request):#添加
    return render(request, 'lib/placelist_admin.html')

def add(request):#添加
    if request.method == 'POST':
        name = request.POST['name']
        address =  request.POST['address']
        time = request.POST['time']
        introduce = request.POST['introduce']
        image= request.FILES['image']
        print( request.FILES);
        # 查询用户是否在数据库中
        print("%s,%s,%s,%s,%s"%(name, introduce,address,time,image))
        if name!="":
            print("3333333333333333333333")
            place=Places(name=name.encode('utf-8'),introduce=introduce.encode('utf-8'),address=address.encode('utf-8'),\
                time=time.encode('utf-8'),image=image)
            place.save()
            print("444444444444444444444444444444" )
            return render(request, 'pages/placelist_add.html',  {'add': '添加成功'})
        else:
            # return HttpResponse('用户不存在')
            return render(request, 'pages/placelist_add.html', {'name': '名称不能为空'})