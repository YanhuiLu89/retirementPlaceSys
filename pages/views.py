from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import Q 

from .models import Users,Places,Scenicspot,Shares
import time
import json

# Create your views here.
##########################################公共接口################################################################
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
                place_list = Places.objects.all().order_by('-publishtime')
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

def home(request):#去首页
    print("2222222222222222222222222222222222222222")
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    username=json.loads(cook)
    user = Users.objects.get(name = username)
    place_list = Places.objects.all().order_by('-publishtime')
    context = {'place_list': place_list}
    if user.usertype == 0:
        return render(request, 'pages/homepage.html',context)
    elif user.usertype == 1:
        print("11111111111111111111111111111111111111111111111111111111111111111")
        return render(request, 'pages/homepage_a.html',context)

def myinfo(request):#我的界面
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    username=json.loads(cook)
    user = Users.objects.get(name = username)
    content={'my':user}
    if user.usertype==0:
        return render(request, 'pages/my.html',content)
    elif user.usertype==1:
        return render(request, 'pages/my_a.html',content)

def editmyinfo(request):#我的界面
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    username=json.loads(cook)
    user = Users.objects.get(name = username)
    if request.method == 'POST':
        temp_name=request.POST.get('name')
        temp_email=request.POST.get('email')
        temp_phone=request.POST.get('phone')
        temp_address=request.POST.get('address')
        user.name=temp_name
        user.email=temp_email
        user.phone=temp_phone
        user.address=temp_address
        user.save()
        return HttpResponseRedirect(reverse('pages:myinfo'))
    content={'my':user}
    return  render(request,'pages/editmyinfo.html',content)

def placedetail(request,place_id):#我的界面
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    context={'place':place}
    return  render(request,'pages/placedetail.html',context)

##########################################管理员相关接口################################################################
def addplace(request):#添加地点页面
    print('addplace:', addspot)
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
        temp_traffic_str=' '.join(temp_traffic_list)
        print('traffic:',temp_traffic_str)
        temp_price= request.POST.get('price')
        temp_spotticket= request.POST.get('spotticket')
        temp_hospital= request.POST.get('hospital')
        print('temp_hospital:',temp_hospital)

        if Places.objects.filter(name=temp_name).exists():
            messages.add_message(request,messages.ERROR,'该课题已经存在')
            return render(request, 'pages/admin_addplace.html')
        else:
            place=Places(name=temp_name,keywords=temp_keywords,introduce=temp_introduce,cost=temp_cost,\
                traffic=temp_traffic_str,price=temp_price,spotticket=temp_spotticket,\
                hospital=temp_hospital,publishtime=timezone.now())
            place.save()
            return HttpResponseRedirect(reverse('pages:home'))#重定向到首页，显示新添加的内容

        return render(request, 'pages/admin_addplace.html')
    return render(request,'pages/admin_addplace.html')

def delplace(request,place_id):#删除地点
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    Places.objects.filter(id=temp_id).delete()
    return HttpResponseRedirect(reverse('pages:home'))

def editplace(request,place_id):#编辑地点
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    if request.method == 'POST':
        place.name = request.POST['name']
        place.keywords =request.POST['keywords']
        place.introduce = request.POST['introduce']
        place.cost= int(request.POST['cost'])
        temp_traffic_list= request.POST.getlist('traffic') 
        place.traffic=' '.join(temp_traffic_list)
        place.price= request.POST.get('price')
        place.spotticket= request.POST.get('spotticket')
        place.hospital= request.POST.get('hospital')
        place.publishtime=timezone.now()
        place.save()
        return HttpResponseRedirect(reverse('pages:home'))#重定向到首页，显示新修改的内容
    content={'place':place}
    return render(request,'pages/admin_editplace.html',content)

def addspot(request):#添加景点页面

    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    place_list=Places.objects.all().order_by('publishtime')
    content={'place_list':place_list}
    if request.method == 'POST':
        temp_name = request.POST['name']
        temp_place=Places.objects.get(name=request.POST['placename'])
        temp_address =request.POST['address']
        temp_opentime =request.POST['time']
        temp_introduce = request.POST['introduce']
        if 'image' in request.FILES:
            temp_image=request.FILES['image']
        else:
            temp_image=''
        if Scenicspot.objects.filter(name=temp_name).exists():
            messages.add_message(request,messages.ERROR,'该景点已经存在')
            return render(request, 'pages/admin_addspot.html',content)
        else:
            scenicspot=Scenicspot(place=temp_place,name=temp_name,introduce=temp_introduce,\
                address=temp_address,opentime=temp_opentime,image=temp_image)
            scenicspot.save()
            messages.add_message(request,messages.INFO,'添加成功，可继续添加')
            return render(request, 'pages/admin_addspot.html',content)
        return render(request, 'pages/admin_addplace.html')
    print('addspot1:' ,addspot)
    return render(request,'pages/admin_addspot.html',content)

#管理用户
def mguser(request):
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user_list = Users.objects.filter(usertype=0).order_by('-id')#只管理非管理员账户
    context = {'user_list': user_list}
    return render(request, 'pages/mguser.html',context)

def deluser(request,user_name):
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_name=user_name
    Users.objects.filter(name=temp_name).delete()
    return HttpResponseRedirect(reverse('pages:mguser'))

#########################################用户相关接口#################################################################
def searchplace(request):#搜索养老地
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    if request.method == 'POST':
        if 'search' in request.POST:#搜索
            searchcontent=request.POST['search_content']
            place_list=Places.objects.filter(Q(name__contains=searchcontent) | Q(keywords__contains=searchcontent) \
                | Q(introduce__contains=searchcontent)|Q(cost__contains=searchcontent)|Q(traffic__contains=searchcontent)\
                |Q(price__contains=searchcontent)|Q(spotticket__contains=searchcontent)|Q(hospital__contains=searchcontent))\
                .order_by('-publishtime') #从各个字段中搜索要搜索的内容
            context = {'place_list': place_list}
            messages.add_message(request,messages.INFO,'共'+str(len(place_list))+'条结果')
            return render(request, 'pages/homepage.html',context)
        elif 'highsearch' in request.POST:#高级搜索
            place_list = Places.objects.all()
            context = {'place_list': place_list}
            return render(request, 'pages/highsearch.html',context)
    return render(request, 'pages/homepage.html')

def highsearch(request):#高级筛选养老地
    cook = request.COOKIES.get('username')
    if cook == None:
        return  render(request, 'pages/index.html')
    print('post:', request.POST)
    filter_count=0
    place_list=Places.objects.all()
    if request.method == 'POST':
        temp_keyword=request.POST['keywords']
        if temp_keyword!=None and temp_keyword!='':
            place_list=place_list.filter(keywords__contains=temp_keyword)
            filter_count+=1

        temp_cost= request.POST['cost']
        if temp_cost!=None and temp_cost!='':
            temp_cost= int(temp_cost)
            print('temp_cost',temp_cost)
            place_list=place_list.filter(cost__range=(temp_cost-500,temp_cost+500))#对于cost的搜索上下500
            filter_count+=1

        temp_traffic_list= request.POST.getlist('traffic') 
        if temp_traffic_list!=None and len(temp_traffic_list)>0:
            temp_traffic_str=' '.join(temp_traffic_list)
            place_list=place_list.filter(traffic__contains=temp_traffic_str)#
            filter_count+=1

        temp_price= request.POST.get('price')
        if temp_price!=None and temp_price!='':
            place_list=place_list.filter(price=temp_price)#
            filter_count+=1

        temp_spotticket= request.POST.get('spotticket')
        if temp_spotticket!=None and temp_spotticket!='':
            place_list=place_list.filter(spotticket=temp_spotticket)#
            filter_count+=1

        temp_hospital= request.POST.get('hospital')
        if temp_hospital!=None and temp_hospital!='':
            place_list=place_list.filter(hospital=temp_hospital)#
            filter_count+=1
        if filter_count==0:
            messages.add_message(request,messages.ERROR,'至少要有一个筛选条件')
            context = {'place_list': contex}
            return render(request, 'pages/highsearch.html',context)
        if len(place_list)==0:
            messages.add_message(request,messages.ERROR,'没有符合条件的搜索结果')
        else:
            messages.add_message(request,messages.INFO,'共'+str(len(place_list))+'条结果')
            place_lsit=place_list.order_by('-publishtime')
            context = {'place_list': place_list}
            return render(request, 'pages/highsearch.html',context)
    return render(request, 'pages/highsearch.html')

def searchspot(request,place_id):#搜索某个地点包含的景点
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    spotlist=Scenicspot.objects.filter(place=place)
    count=len(spotlist)
    content={'count':count,'spot_list':spotlist}
    return render(request,'pages/spotlist.html',content)

def retiregroup(request):#养老圈
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    sharelist=Shares.objects.all().order_by('-time')
    context={'share_list':sharelist}
    return render(request, 'pages/retiregroup.html',context)

def toshareplace(request,place_id):#分享到养老圈
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    username=json.loads(cook)
    user = Users.objects.get(name = username)
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    context={'place':place}
    return render(request, 'pages/share.html',context)

def shareplace(request,place_id):#分享到养老圈
    cook = request.COOKIES.get('username')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    if request.method == 'POST':
        username=json.loads(cook)
        user = Users.objects.get(name = username)
        temp_text=request.POST['text']
        if 'image' in request.FILES:
            temp_image=request.FILES['image']
        else:
            temp_image=''
        share=Shares(user=user,place=place,text=temp_text,image=temp_image,time=timezone.now())
        share.save()
        return HttpResponseRedirect(reverse('pages:retiregroup'))
    context={'place':place}
    return render(request, 'pages/share.html',context)
    
