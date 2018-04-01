## Docker flask based on flask app ##

主要功能：以容器形式封装flask，nginx和uwsgi  
启动方式：`docker-compose up -d`  
停止方式：`docker-compose down`   
访问方式：浏览器访问0.0.0.0:80  

[基础镜像：tiangolo/uwsgi-nginx-flask-docker](https://github.com/tiangolo/uwsgi-nginx-flask-docker)

### 基本概述 ###
- `main.py`：app的主入口，负责启动app并设置url路径和对应的函数
- `models.py`：存在所有的数据定义，注意MongoDB的引擎设置也在其中
- `views.py`：存放所有web页面的函数，在`main.py`使用app.add_route_rule方法
- `settings.py`：新增，用于保存flask所需要的配置，包含mongo等
- `uwsgi.ini`：uwsgi配置文件，用于连接Nginx和Flask
- `requirements.txt`：定义Flask所需要的第三方类库，在创建container时自动安装
- `static/`：存放所有静态文件的目录，这也是flask唯一存放静态文件的目录
    >- `bootstrap/`:bootstrap v4.0的库文件，包含css和js
    >- `imags/`:自定义的图像文件
    >- `js/`:自定义的js脚本
- `templates/`: 存放所有html模版的目录，基于jinja2

