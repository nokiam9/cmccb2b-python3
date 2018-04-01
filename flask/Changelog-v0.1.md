## flask v0.1 201804 ###

### 开发记录 ###
- 现在的开发基于python3.6
- 修复pymongo的connect有时失败的bug，MongoClient设置connect＝False，不立即connect mongo
- 修改`main.py`，将@`app.route()`修饰符方式改为`app.add_url_rule()`方式，并将所有页面函数隐藏到`views.py`
- 修改`pagination.html`，点击记录时打开新开窗口显示招标详情，且对未设置提醒的记录改变字体颜色
- 增加查询专用index，解决pagination内存溢出问题
- 增加了`requirement.txt`, 说明自定义需要补充的类库，
实际在Dockerfile中手工增加了RUN指令
- 将requirement.txt的位置调整到app_0_2的目录，
以便控制不同版本app的类库依赖，同时修改了Dockerfile的加载顺序，
先向容器中拷入该文件，然后自动进行全部依赖类库的pip安装，
不再需手工设置

### 后续任务 ###
- 开发基于按时分布的新项目数量图表，考虑charts.js
- 考虑flask采用https取代http

### 经验之谈  ###
- 创建本容器时，注意在Dcokfile中设置app不同版本所在的目录  
- 注意：本机开发时settings.py中mongo.db设置为0.0.0.0，但在docker-compose时应修改为mongo；
并注意app的port应修改为80，本机测试可以取3000等
- 修复pymongo的[connect bug](https://www.cnblogs.com/dhcn/p/7121395.html)，settings.py增加`connect=False`设置
- 解决三个容器之间的通信需求，links已经不再作为docker的推荐方式，建议首选
network方式，但是共享nework需要在多个compose的外部创建`$ docker network create ap_domain`，
而且在compose内部使用一级network指令创建时，
自动给name添加目录名（例如mongoap_ap_domain）
- docker方式，只能用app装饰的方法，app.add_url_rule都无法找到uwsgi的应用（已解决，实际上是flask与uwsgi的协同方式的影响）














