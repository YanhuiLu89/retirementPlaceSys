from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):#index,首页
    print ('000000000')
    if request.method == 'POST':     
        if 'regist' in request.POST:
            print ('111111111111111111111111111')
            return render(request, 'pages/regist.html')#跳转到注册页面    
        elif  'login' in request.POST: 
            print ('222222222222222222222')
            return render(request, 'pages/login.html')#跳转到登陆页面     
    print ('3333333333333333333333333')    
    return render(request, 'pages/index.html')

def toregist(request):#去注册页面
    return render(request, 'pages/index.html')

def tologin(request):#去登陆页面
    return render(request, 'pages/index.html')

def regist(request):#注册
    return render(request, 'pages/regist.html')

def login(request):#登陆
    return render(request, 'pages/login.html')