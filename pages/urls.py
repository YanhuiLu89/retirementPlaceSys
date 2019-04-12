from django.urls import path
from . import views

app_name='[pages]'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('regist/', views.regist, name='regist'),
    path('login/', views.login, name='login'),
    path('homepage/', views.placelist, name='placelist'),
    path('admin_addplace/', views.add, name='add'),
    path('placelist_add/', views.toadd, name='toadd'),
    path('placelist_add/', views.toview, name='toview'),
]