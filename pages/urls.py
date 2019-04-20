from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='[pages]'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('addspot/', views.addspot, name='addspot'),
    path('addplace/', views.addplace, name='addplace'),
    path('delplace/<place_id>', views.delplace, name='delplace'),
    path('editplace/<place_id>', views.editplace, name='editplace'),
    path('mguser/', views.mguser, name='mguser'),
    path('deluser/<user_name>', views.deluser, name='deluser'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('editmyinfo/', views.editmyinfo, name='editmyinfo'),
    path('home/', views.home, name='home'),
    path('searchplace/', views.searchplace, name='searchplace'),
    path('highsearch/', views.highsearch, name='highsearch'),
    path('retiregroup/', views.retiregroup, name='retiregroup'),
    path('shareplace/<place_id>', views.shareplace, name='shareplace'),
    path('searchsport/<place_id>', views.searchspot, name='searchspot'),
]