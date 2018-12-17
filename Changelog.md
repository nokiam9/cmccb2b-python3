# 开发记录

## V1.4 on 2018.12

- **重大变化**：docker集群仅提供http，由Host主机的NGINX统一支持https，并指向docker中不同容器提供反向代理；
- 启用 www.caogo.cn、scrapy.caogo.cn、xunsearch.caogo.cn 3个站点，并相应修改html和php
- 重构docker-compose，修改container的名字，数据目录修改为cmdata
- nginx改造为proxy，crontab改为cronjobs
- cronjobs的定时xunsearch索引更新改为curl方式，并修改php文件解决前台运行超过30s中断的问题

---

- 本地测试时需要修改/etc/host，将3个站点指向localhost, docker-compose.yml中cm-proxy必须暴露80端口
- ECS生产环境部署时，可以修改docker-compose.yml中cm-proxy的自定义暴露端口，并响应修改系统级NGINX的proxy.conf配置
- mongo的container name还没有修改

## V1.3 on 2018.8.16

- flask的图表展示bug fix

## V1.2 on 2018.8.16

- b2b.10086.cn于2018.8.10网站升级，增加了User-Agent格式和Referer跨站脚本的检测功能，并调整了notice_type
- 由于notice_type有变化，mongo历史数据可能混乱，flask的UI菜单未修改，

## 开发记录 2018.04

- 建立venv/的virtualenv，启动方式为`$ source venv/bin/activate`，退出方式为`$ deactivate`
- 新增`.gitignore`, 避免git引入开发过程文件
- 新增`workspace/`，用于一些临时测试和开发，通过后调整到正式文件
- 将`user_date/` 改名`data/`
- scrapy的logs改为docker volume方式，不再保存
- 修改`prestart.sh`，增加`-dev`参数，mongo补充启动docker-compose的override文件，以打开外部IP访问
- 修改`setup.sh`，将mongo/migrations的样本数据该用管道处理避免文件解压，并将目录设为只读，以便控制GitHub的数据量

## 遗留问题

- `pip install scrpay`有bug，必须提前安装`incremental`(manage python project version )
- `pip install flask-mongoengine`有bug，必须提前安装nose, rednose, converage
