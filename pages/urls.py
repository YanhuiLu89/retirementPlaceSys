from django.urls import path
from . import views

app_name='[pages]'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('addplace/', views.addplace, name='addplace'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('home/', views.home, name='home'),
    path('addspot/', views.addspot, name='addspot'),
]