from django.urls import path
from . import views

app_name='[pages]'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('addplace/', views.addplace, name='addplace'),
    path('delplace/<place_name>', views.delplace, name='delplace'),
    path('editplace/<place_name>', views.editplace, name='editplace'),
    path('mguser/', views.mguser, name='mguser'),
    path('deluser/<user_name>', views.deluser, name='deluser'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('editmyinfo/', views.editmyinfo, name='editmyinfo'),
    path('home/', views.home, name='home'),
    path('addspot/', views.addspot, name='addspot'),
    path('searchplace/', views.searchplace, name='searchplace'),
    path('highsearch/', views.highsearch, name='highsearch'),
    path('retiregroup/', views.retiregroup, name='retiregroup'),
    path('shareplace/<place_name>', views.shareplace, name='shareplace'),
]