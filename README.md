﻿# retirementPlaceSys
基于django的海南省候鸟式养老系统
# django-python
运行步骤
1、安装python3.7,并配置到环境变量

2、安装mysql数据库（5.7及以上版本），并启动数据库服务

3、安装所需模块:在命令行依次执行以下输入
	pip install django
	pip install mysqlclient
	pip install Pillow
(注意	1、如果执行第二步时出现类似“。。。。。pip install --upgrade pip”的错误，按提示执行以下命令：pip install --upgrade pip
	2、如果pip install mysqlclient出现错误就执行pip install mysqlclient-1.4.4-cp37-cp37m-win_amd64.whl)

4、创建数据数据库，注意编码格式：
create database retirement_place_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

5、同步数据库，在retirementPlaceSys路径依次执行以下命令：
    manage.py makemigrations
    manage.py sqlmigrate pages 0001
    manage.py migrate
6、创建管理员账户，管理员是不能注册的。从命令行进入graduationDesignSys路径，依次执行以下命令
	python manage.py shell
	>>> from pages.models import Users
	>>> from pages.models import AdminInfos;
	>>> admin=Users(usertype=1,name='admin01',password='123456',email="296932576@qq.com")
	>>> admin.save()
	ctrl-z退出 shell命令

7、从命令行进入到retirementPlaceSys路径，执行python manage.py runserver,出现Starting development server at http://127.0.0.1:8000/之后，
    在浏览器地址栏输入http://127.0.0.1:8000/pages/index/进入首页，首页有登录和注册入口

   