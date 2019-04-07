from django.urls import path
from . import views

app_name='[pages]'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('regist/', views.regist, name='regist'),
    path('login/', views.login, name='login'),
    path('placelist/', views.placelist, name='placelist'),
]