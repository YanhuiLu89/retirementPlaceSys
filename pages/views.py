from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):#index,首页
    return render(request, 'pages/index.html')

def toregist(request):#去注册页面
    return render(request, 'pages/index.html')

def tologin(request):#去登陆页面
    return render(request, 'pages/index.html')

def regist(request):#注册
    return render(request, 'pages/index.html')

def login(request):#登陆
    return render(request, 'pages/index.html')