from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils import timezone

from .models import Users,Places
import time
import json

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
                place_list = Places.objects.all()
                context = {'place_list': place_list}
                request.session['is_login'] = 'true'
                request.session['username'] = user.name
                if user.usertype==1:
                    response=render(request, 'pages/homepage_a.html',context)#跳到管理员首页界面
                else:
                    response=render(request, 'pages/homepage.html',context)#跳到会员首页界面
                #set cookie
                response.set_cookie('username', json.dumps(user.name))#中文字符串直接设置到cooki有问题要用json转一下
                return response
            else:
                messages.add_message(request,messages.ERROR,'用户密码或身份类型错误错误')
                return render(request, 'pages/login.html')
        else:
            print("333333333333333333333")
            messages.add_message(request,messages.ERROR,'用户不存在')
            return render(request, 'pages/login.html')
    return render(request, 'pages/login.html')

def logout(request):#退出
    request.session.delete()
    request.session.flush() 
    response=render(request, 'pages/index.html')
    response.delete_cookie("username")
    return response

def addspot(request):#添加景点界面
    return render(request, 'pages/admin_addplace.html')

def home(request):#去首页
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    username=json.loads(cook)
    user = Users.objects.get(name = username)
    place_list = Places.objects.all()
    context = {'place_list': place_list}
    if user.usertype == 0:
        return render(request, 'pages/homepage.html',context)
    elif user.usertype == 1:
        return render(request, 'pages/homepage_a.html',context)

def myinfo(request):#我的界面
    return render(request, 'pages/homepage.html')

def addplace(request):#添加地点页面
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    if request.method == 'POST':
        temp_name = request.POST['name']
        temp_keywords =request.POST['keywords']
        temp_introduce = request.POST['introduce']
        temp_cost= int(request.POST['cost'])
        temp_traffic_list= request.POST.getlist('traffic') 
        print('traffic:',temp_traffic_list)
        temp_price= (int)(request.POST.get('price'))
        print('temp_price:',temp_price)
        temp_spotticket= (int)(request.POST.get('spotticket'))
        temp_hospital= (bool)(request.POST.get('hospital'))
        print('temp_hospital:',temp_hospital)

        if Places.objects.filter(name=temp_name).exists():
            messages.add_message(request,messages.ERROR,'该课题已经存在')
            return render(request, 'pages/admin_addplace.html')
        else:
            place=Places(name=temp_name,keywords=temp_keywords,introduce=temp_introduce,cost=temp_cost,\
                traffic_highrail='highrail' in temp_traffic_list,traffic_air='air' in temp_traffic_list,\
                traffic_port='port' in temp_traffic_list,price=temp_price,spotticket=temp_spotticket,\
                hashospital=temp_hospital,publishtime=timezone.now())
            place.save()
            return HttpResponseRedirect(reverse('pages:home'))#重定向到首页，显示新添加的内容

        return render(request, 'pages/admin_addplace.html')
    return render(request,'pages/admin_addplace.html')

def delplace(request,place_name):#删除地点
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_name=place_name
    Places.objects.filter(name=temp_name).delete()
    return HttpResponseRedirect(reverse('pages:home'))

def editplace(request,place_name):#编辑地点
    return HttpResponseRedirect(reverse('pages:home'))