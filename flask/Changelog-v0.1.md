## flask v0.1 201804 ###

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

### 开发记录 ###
- 现在的开发基于python3.6
- 修复pymongo的connect有时失败的bug，MongoClient设置connect＝False，不立即connect mongo
- 修改`main.py`，将@`app.route()`修饰符方式改为`app.add_url_rule()`方式，并将所有页面函数隐藏到`views.py`
- 修改`pagination.html`，点击记录时打开新开窗口显示招标详情，且对未设置提醒的记录改变字体颜色
- 增加查询专用index，解决pagination内存溢出问题

### 后续任务 ###
- 开发基于按时分布的新项目数量图表，考虑charts.js
- 考虑flask采用https取代http






