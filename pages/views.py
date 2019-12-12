from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import Q 

from .models import Users,Places,Scenicspot,Shares,Order,Comment,Like
import time

# Create your views here.
##########################################公共接口################################################################
def index(request):#入口页
    if request.method == 'POST':  
        temp_name = request.POST['username']
        temp_psw = request.POST['password']
        temp_mail = request.POST['mail']
        temp_usertype = int(request.POST['usertype'])
        print( temp_name+","+temp_psw+","+temp_mail)
        if Users.objects.filter(name=temp_name).exists():
            messages.add_message(request,messages.ERROR,'该用户名已经存在')
            return render(request,'pages/index.html')
        if Users.objects.filter(email=temp_mail).exists():
            messages.add_message(request,messages.ERROR,'该邮箱已经注册过')
            return render(request,'pages/index.html')
        user = Users(usertype=temp_usertype,name=temp_name, password=temp_psw, email=temp_mail)
        user.save()
        if 2==temp_usertype:#如果是养老机构会员，要创建对应的养老机构对象
            place=Places(user=user,name=user.name,publishtime=timezone.now(),)
            place.save()
        return render(request,'pages/login.html')
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
            if user.password==password and int(user.usertype)==usertype:
                print("2222222222222222222")
                place_list = Places.objects.all().order_by('-publishtime')
                context = {'place_list': place_list}
                request.session['is_login'] = 'true'
                request.session['usermail'] = user.email
                if user.usertype==1:
                    response=render(request, 'pages/homepage_a.html',context)#跳到管理员首页界面
                elif user.usertype==2:
                    response=render(request, 'pages/homepage_c.html',context)#跳到养老机构首页界面
                else:
                    response=render(request, 'pages/homepage.html',context)#跳到会员首页界面
                #set cookie
                response.set_cookie('usermail', user.email)
                return response
            else:
                messages.add_message(request,messages.ERROR,'用户密码或身份类型错误')
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
    response.delete_cookie("usermail")
    return response

def home(request):#去首页
    cook = request.COOKIES.get('usermail')
    if cook == None:
        return  render(request, 'pages/index.html')
    place_list = Places.objects.filter().order_by('-publishtime')
    context = {'place_list': place_list}
    user = Users.objects.get(email = cook)
    if user.usertype == 0:
        return render(request, 'pages/homepage.html',context)
    elif user.usertype == 1:
        return render(request, 'pages/homepage_a.html',context)
    elif user.usertype == 2:
        return render(request, 'pages/homepage_c.html',context)

def myinfo(request):#我的界面
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user = Users.objects.get(email = cook)
    if user.usertype==0:
        order_list=Order.objects.filter(user=user).order_by('-time')
        content={'my':user,'order_list':order_list}
    elif user.usertype==1:
        content={'my':user}
    if user.usertype==2:
        place=Places.objects.get(user=user)
        order_list=Order.objects.filter(place=place).order_by('-time')
        content={'my':user,'order_list':order_list}
    if user.usertype==0:
        return render(request, 'pages/my.html',content)
    elif user.usertype==1:
        return render(request, 'pages/my_a.html',content)
    elif user.usertype==2:
        return render(request, 'pages/my_c.html',content)

def editmyinfo(request):#我的界面
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user = Users.objects.get(email = cook)
    if request.method == 'POST':
        temp_name=request.POST.get('name')
        temp_phone=request.POST.get('phone')
        temp_address=request.POST.get('address')
        user.name=temp_name
        user.phone=temp_phone
        user.address=temp_address
        user.save()
        return HttpResponseRedirect(reverse('pages:myinfo'))
    content={'my':user}
    if user.usertype==0:
        return  render(request,'pages/editmyinfo.html',content)
    elif user.usertype==1:
        return  render(request,'pages/editmyinfo_a.html',content)
    elif user.usertype==2:
        return render(request, 'pages/editmyinfo_c.html',content)

def placedetail(request,place_id):#我的界面
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    context={'place':place}
    return  render(request,'pages/placedetail.html',context)

##########################################管理员相关接口################################################################d
def mgplace(request):
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    place_list = Places.objects.all().order_by('-publishtime')
    context = {'place_list': place_list}
    return render(request, 'pages/mgplace.html',context)#跳到地点管理界面

def mgspot(request):
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    spot_list = Scenicspot.objects.all().order_by('-id')
    context = {'spot_list': spot_list}
    return render(request, 'pages/mgspot.html',context)#跳到地点管理界面

def addplace(request):#添加地点页面
    cook = request.COOKIES.get('usermail')
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
            messages.add_message(request,messages.ERROR,'该y=养老机构已经存在')
            return render(request, 'pages/admin_addplace.html')
        else:
            place=Places(name=temp_name,keywords=temp_keywords,introduce=temp_introduce,cost=temp_cost,\
                traffic=temp_traffic_str,price=temp_price,spotticket=temp_spotticket,\
                hospital=temp_hospital,publishtime=timezone.now())
            place.save()
            return HttpResponseRedirect(reverse('pages:mgplace'))
    return render(request, 'pages/admin_addplace.html')

def delplace(request,place_id):#删除地点
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    Places.objects.filter(id=temp_id).delete()
    return HttpResponseRedirect(reverse('pages:mgplace'))

def editplace(request,place_id):#编辑地点
    cook = request.COOKIES.get('usermail')
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
        return HttpResponseRedirect(reverse('pages:mgplace'))#重定向到首页，显示新修改的内容
    content={'place':place}
    return render(request,'pages/admin_editplace.html',content)

def addspot(request):#添加景点页面

    cook = request.COOKIES.get('usermail')
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
            return HttpResponseRedirect(reverse('pages:mgspot'))
        return render(request, 'pages/admin_addplace.html')
    print('addspot1:' ,addspot)
    return render(request,'pages/admin_addspot.html',content)

def editspot(request,spot_id):
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=spot_id
    spot=Scenicspot.objects.get(id=temp_id)
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
        spot.name=temp_name
        spot.place=temp_place
        spot.introduce=temp_introduce
        spot.address=temp_address
        spot.opentime=temp_opentime
        spot.image=temp_image
        spot.save()
        return HttpResponseRedirect(reverse('pages:mgspot'))
    placelist=Places.objects.all()
    context={'spot':spot,'place_list':placelist}
    return render(request,'pages/admin_editspot.html',context)

def delspot(request,spot_id):   
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=spot_id
    Scenicspot.objects.filter(id=temp_id).delete()
    return HttpResponseRedirect(reverse('pages:mgspot'))

#管理用户
def mguser(request):
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user_list = Users.objects.filter(usertype=0).order_by('-id')#只管理非管理员账户
    context = {'user_list': user_list}
    return render(request, 'pages/mguser.html',context)

def deluser(request,user_id):
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=user_id
    Users.objects.filter(id=temp_id).delete()
    return HttpResponseRedirect(reverse('pages:mguser'))

#########################################用户相关接口#################################################################
def searchplace(request):#搜索养老地
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user = Users.objects.get(email = cook)
    if request.method == 'POST':
        if 'search' in request.POST:#搜索
            searchcontent=request.POST['search_content']
            place_list=Places.objects.filter(Q(name__contains=searchcontent) | Q(keywords__contains=searchcontent) \
                | Q(introduce__contains=searchcontent)|Q(cost__contains=searchcontent)|Q(traffic__contains=searchcontent)\
                |Q(price__contains=searchcontent)|Q(spotticket__contains=searchcontent)|Q(hospital__contains=searchcontent)\
                |Q(phone__contains=searchcontent)|Q(address__contains=searchcontent))\
                .order_by('-publishtime') #从各个字段中搜索要搜索的内容
            context = {'place_list': place_list}
            messages.add_message(request,messages.INFO,'共'+str(len(place_list))+'条结果')
            if user.usertype==0:
                return  render(request,'pages/homepage.html',context )
            elif user.usertype==1:
                return  render(request,'pages/homepage_a.html',context )
            elif user.usertype==2:
                return render(request, 'pages/homepage_c.html',context )
        elif 'highsearch' in request.POST:#高级搜索
            place_list = Places.objects.all()
            context = {'place_list': place_list}
            return HttpResponseRedirect(reverse('pages:highsearch'))
    return render(request, 'pages/homepage.html')

def highsearch(request):#高级筛选养老地
    cook = request.COOKIES.get('usermail')
    if cook == None:
        return  render(request, 'pages/index.html')
    print('post:', request.POST)
    user = Users.objects.get(email = cook)
    filter_count=0
    place_list=Places.objects.all().order_by('-publishtime')
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
            if user.usertype == 0:
                return render(request, 'pages/highsearch.html',context)
            elif user.usertype == 2:
                return render(request, 'pages/highsearch_c.html',context)
        if len(place_list)==0:
            messages.add_message(request,messages.ERROR,'没有符合条件的搜索结果')
        else:
            messages.add_message(request,messages.INFO,'共'+str(len(place_list))+'条结果')
            place_lsit=place_list.order_by('-publishtime')
            context = {'place_list': place_list}
            if user.usertype == 0:
                return render(request, 'pages/highsearch.html',context)
            elif user.usertype == 2:
                return render(request, 'pages/highsearch_c.html',context)
    context = {'place_list': place_list}
    if user.usertype == 0:
        return render(request, 'pages/highsearch.html',context)
    elif user.usertype == 2:
        return render(request, 'pages/highsearch_c.html',context)

def localspot(request,place_id):#当地景点
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    spotlist=Scenicspot.objects.filter(place=place)
    count=len(spotlist)
    content={'count':count,'spot_list':spotlist}
    return render(request,'pages/spotlist.html',content)

def searchspot(request):#景点搜索页面，按关键字搜索
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user = Users.objects.get(email = cook)
    if request.method == 'POST':
        searchcontent=request.POST['search_content']
        spot_list=Scenicspot.objects.filter(Q(name__contains=searchcontent) | Q(introduce__contains=searchcontent)|Q(address__contains=searchcontent)) #从名称、简介、地址字段中搜索要搜索的内容
        if len( spot_list)==0:
            messages.add_message(request,messages.ERROR,'没有符合条件的搜索结果')
        else:
            messages.add_message(request,messages.INFO,'共'+str(len( spot_list))+'条结果')
            content={'spot_list':spot_list}
            if user.usertype == 0:
                return render(request,'pages/searchspot.html',content)
            elif user.usertype == 2:
                return render(request,'pages/searchspot_c.html',content)

    spot_list=Scenicspot.objects.all()
    content={'spot_list':spot_list}
    if user.usertype == 0:
        return render(request,'pages/searchspot.html',content)
    elif user.usertype == 2:
        return render(request,'pages/searchspot_c.html',content)
    

def retiregroup(request):#养老圈
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user = Users.objects.get(email = cook)
    sharelist=Shares.objects.all().order_by('-time')
    content={'share_list':sharelist}
    if user.usertype == 0:
        return render(request,'pages/retiregroup.html',content)
    elif user.usertype == 2:
        return render(request,'pages/retiregroup_c.html',content)

def toshareplace(request,place_id):#分享到养老圈
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    user = Users.objects.get(email = cook)
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    context={'place':place}
    return render(request, 'pages/share.html',context)

def shareplace(request,place_id):#分享到养老圈
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    if request.method == 'POST':
        user = Users.objects.get(email = cook)
        temp_text=request.POST['text']
        if 'image' in request.FILES:
            temp_image=request.FILES['image']
        else:
            temp_image=''
        share=Shares(user=user,place=place,text=temp_text,image=temp_image,time=timezone.now())
        share.save()
        place.sharedcount+=1
        place.save()
        return HttpResponseRedirect(reverse('pages:retiregroup'))
    context={'place':place}
    return render(request, 'pages/share.html',context)

def likeplace(request,place_id):#点赞某个养老机构
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    currentUser = Users.objects.get(email = cook)
    temp_id=place_id
    currentPlace=Places.objects.get(id=temp_id)
    if Like.objects.filter(Q(user=currentUser) & Q(place=currentPlace)).exists():
        Like.objects.filter(Q(user=currentUser) & Q(place=currentPlace)).delete()
        currentPlace.likedcount-= 1
    else:
        like=Like(user=currentUser,place=currentPlace,time=timezone.now())
        like.save()
        currentPlace.likedcount+= 1
    currentPlace.save()
    return HttpResponseRedirect(reverse('pages:home'))#重定向到首页，显示新修改的内容

def makeorder(request,place_id,room_kind):#订单
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    currentPlace=Places.objects.get(id=temp_id)
    currentUser = Users.objects.get(email = cook)
    if request.method == 'POST':
        temp_checkin = request.POST['checkin']
        temp_checkout = request.POST['checkout']
        temp_guestname=request.POST['guestname']
        temp_phone=request.POST['phone']
        temp_guestcount=request.POST['guestcount']
        temp_roomcount=request.POST['roomcount']
        temp_fee=0
        if room_kind==0:
            temp_fee=currentPlace.singleroomfee*temp_roomcount
        elif room_kind==1:
            temp_fee=currentPlace.doubleroomfee*temp_roomcount
        elif room_kind==2:
            temp_fee=currentPlace.familyroomfee*temp_roomcount
        order=Order(user=currentUser,place=currentPlace,roomkind=room_kind,roomcount=temp_roomcount,phone=temp_phone,guestname=temp_guestname,\
                guestcount= temp_guestcount,checkintime=temp_checkin,checkouttime=temp_checkout,fee=temp_fee,time=timezone.now())
        order.save()
        messages.add_message(request,messages.INFO,'订单已提交，待商家确认')
        return HttpResponseRedirect(reverse('pages:myinfo'))#重定向到我的页面
    content={'place_id':currentPlace.id,'room_kind':room_kind,'place':currentPlace}
    return render(request,'pages/makeorder.html',content)

def cancelorder(request,order_id):#订单
    print("order_id="+order_id)
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=order_id
    order=Order.objects.get(id=temp_id)
    order.state=2
    order.save()
    messages.add_message(request,messages.INFO,'订单已取消')
    return HttpResponseRedirect(reverse('pages:myinfo'))#重定向到我的页面

#########################################养老机构相关接口#################################################################
def mginfo_c(request):#养老机构信息管理地
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    currentuser=Users.objects.get(email=cook)
    place = Places.objects.get(user=currentuser)
    context = {'place': place}
    return render(request, 'pages/mginfo_c.html',context)#跳到地点管理界面

def editinfo_c(request,place_id):#编辑信息
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=place_id
    place=Places.objects.get(id=temp_id)
    if request.method == 'POST':
        place.name = request.POST['name']
        place.phone=request.POST['phone']
        place.keywords =request.POST['keywords']
        place.introduce = request.POST['introduce']
        place.cost= int(request.POST['cost'])
        temp_traffic_list= request.POST.getlist('traffic') 
        place.traffic=' '.join(temp_traffic_list)
        place.price= request.POST.get('price')
        place.spotticket= request.POST.get('spotticket')
        place.hospital= request.POST.get('hospital')
        place.address = request.POST.get('address')
        place.singleroomcount= request.POST.get('singleroomcount')
        place.singleroomfee= request.POST.get('singleroomfee')
        place.doubleroomcount= request.POST.get('doubleroomcount')
        place.doubleroomfee= request.POST.get('doubleroomfee')
        place.familyroomcount= request.POST.get('familyroomcount')
        place.familyroomfee= request.POST.get('familyroomfee')
        if 'image' in request.FILES:
            place.image=request.FILES['image']
        place.publishtime=timezone.now()
        place.save()
        return HttpResponseRedirect(reverse('pages:mginfo_c'))#重定向到首页，显示新修改的内容
    content={'place':place}
    return render(request,'pages/editinfo_c.html',content)

def mgorder_c(request):#管理订单
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    place_list = Places.objects.all().order_by('-publishtime')
    context = {'place_list': place_list}
    return render(request, 'pages/mgplace.html',context)#跳到地点管理界面

def confirmorder(request,order_id):#订单
    print("order_id="+order_id)
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=order_id
    order=Order.objects.get(id=temp_id)
    order.state=1
    order.save()
    messages.add_message(request,messages.INFO,'订单已确认')
    return HttpResponseRedirect(reverse('pages:myinfo'))#重定向到我的页面
 
def refuseorder(request,order_id):#订单
    print("order_id="+order_id)
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=order_id
    order=Order.objects.get(id=temp_id)
    order.state=3
    order.save()
    messages.add_message(request,messages.INFO,'订单已拒绝')
    return HttpResponseRedirect(reverse('pages:myinfo'))#重定向到我的页面

def finishorder(request,order_id):#订单
    print("order_id="+order_id)
    cook = request.COOKIES.get('usermail')
    print('cook:', cook)
    if cook == None:
        return  render(request, 'pages/index.html')
    temp_id=order_id
    order=Order.objects.get(id=temp_id)
    order.state=4
    order.save()
    messages.add_message(request,messages.INFO,'订单已完成')
    return HttpResponseRedirect(reverse('pages:myinfo'))#重定向到我的页面