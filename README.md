# retirementPlaceSys
基于django的海南省候鸟式养老系统
# django-python
运行步骤
1、安装python3.7,并配置到环境变量
2、安装django:在命令行输入pip install django
3、安装mysql数据库（5.7及以上版本），并启动数据库服务
4、创建数据数据库，注意编码格式：
create database retirement_place_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
5、导入数据:mysql -u username -p retirement_place_db < /.../graduationDesignSys/retirement_place_db.sql
6、同步数据库，在retirementPlaceSys路径依次执行以下命令：
    manage.py makemigrations
    manage.py sqlmigrate pages 0001
    manage.py migrate
7、创建管理员账户，管理员是不能注册的
8、从命令行进入到retirementPlaceSys路径，执行以下命令：
	manage.py runserver,出现Starting development server at http://127.0.0.1:8000/之后，
在浏览器地址栏输入http://127.0.0.1:8000/pages/index/进入首页，首页有登录和注册入口

目前实现功能：注册、登录、重复注册，密码或用户名不对，管理员主界面，管理员添加地点
   