from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='[pages]'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mgspot/', views.mgspot, name='mgspot'),
    path('addspot/', views.addspot, name='addspot'),
    path('delspot/<spot_id>', views.delspot, name='delspot'),
    path('editspot/<spot_id>', views.editspot, name='editspot'),
    path('mgplace/', views.mgplace, name='mgplace'),
    path('addplace/', views.addplace, name='addplace'),
    path('delplace/<place_id>', views.delplace, name='delplace'),
    path('editplace/<place_id>', views.editplace, name='editplace'),
    path('placedetail/<place_id>', views.placedetail, name='placedetail'),
    path('mguser/', views.mguser, name='mguser'),
    path('deluser/<user_id>', views.deluser, name='deluser'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('editmyinfo/', views.editmyinfo, name='editmyinfo'),
    path('home/', views.home, name='home'),
    path('searchplace/', views.searchplace, name='searchplace'),
    path('highsearch/', views.highsearch, name='highsearch'),
    path('retiregroup/', views.retiregroup, name='retiregroup'),
    path('toshareplace/<place_id>', views.toshareplace, name='toshareplace'),
    path('shareplace/<place_id>', views.shareplace, name='shareplace'),
    path('likeplace/<place_id>', views.likeplace, name='likeplace'),
    path('localspot/<place_id>', views.localspot, name='localspot'),
    path('searchspot/', views.searchspot, name='searchspot'),
    path('mginfo_c/', views.mginfo_c, name='mginfo_c'),
    path('editinfo_c/<place_id>', views.editinfo_c, name='editinfo_c'),
    path('magorder_c/', views.mgorder_c, name='mgorder_c'),
    path('makeorder/<place_id><room_kind>', views.makeorder, name='makeorder'),
]