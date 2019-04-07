from django.urls import path
from . import views

app_name='[pages]'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('index/', views.toregist, name='toregist'),
    path('index/', views.tologin, name='tologin'),
    path('login/', views.regist, name='regist'),
    path('regist/', views.login, name='login'),
]