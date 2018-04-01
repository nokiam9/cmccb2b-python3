## Docker flask based on flask app ##

主要功能：以容器形式封装flask，nginx和uwsgi  
启动方式：`docker-compose up -d`  
停止方式：`docker-compose down`   
访问方式：浏览器访问0.0.0.0:80  

### 参考文档 ###
- [tiangolo/uwsgi-nginx-flask:python2.7：基础镜像，集成了flask、uwsgi、nginx](https://github.com/tiangolo/uwsgi-nginx-flask-docker)
- [flask中文资料](http://docs.jinkan.org/docs/flask/)    
- [flask官方网站](http://flask.pocoo.org/docs/0.12/)  
- [jinja2官方文档](http://jinja.pocoo.org/docs/2.10/)
- [bootstrap中文文档](https://v4.bootcss.com/docs/4.0/getting-started/introduction/)
- [html便签](http://www.runoob.com/html/html-quicklist.html)
- [css手册](http://www.runoob.com/css/css-tutorial.html)
- [javascript手册](http://www.runoob.com/js/js-tutorial.html)
- [Mongo engine 源代码](https://github.com/MongoEngine/mongoengine)
- [Mongo Engine 官方文档](https://mongoengine-odm.readthedocs.io/)
- [Flask Mongo Engnie 源代码](https://github.com/MongoEngine/flask-mongoengine)
- [Flask Mongo Engine 官方文档](https://flask-mongoengine.readthedocs.io/en/latest/)





### 注意事项 ###
* 创建本容器时，注意在Dcokfile中设置app不同版本所在的目录  
* 注意：本机开发时settings.py中mongo.db设置为0.0.0.0，但在docker-compose时应修改为mongo；
并注意app的port应修改为80，本机测试可以取3000等
* 修复pymongo的[connect bug](https://www.cnblogs.com/dhcn/p/7121395.html)，settings.py增加`connect=False`设置，
      

### 开发记录 ###
* 增加了`requirement.txt`, 说明自定义需要补充的类库，
实际在Dockerfile中手工增加了RUN指令
* 将requirement.txt的位置调整到app_0_2的目录，
以便控制不同版本app的类库依赖，同时修改了Dockerfile的加载顺序，
先向容器中拷入该文件，然后自动进行全部依赖类库的pip安装，
不再需手工设置
* network的设置还要继续研究，flask container中mongo的IP不是localhost


### 遗留问题 ###
- 解决三个容器之间的通信需求，links已经不再作为docker的推荐方式，建议首选
network方式，但是共享nework需要在多个compose的外部创建`$ docker network create ap_domain`，
而且在compose内部使用一级network指令创建时，
自动给name添加目录名（例如mongoap_ap_domain）

- docker方式，只能用app装饰的方法，app.add_url_rule都无法找到uwsgi的应用？？？
the main application object should be named app (in the code) as in this example.





