# 最新进展 on 2018.12.12

- 启用www.caogo.cn, scrapy.caogo.cn, xunsearch.caogo.cn等3个站点，并相应修改flask和php
- 默认是http方式，未来在ECS的NGINX中采用https；
- 本次测试时需要修改/etc/host，将3个站点指向locaohost
- 重构docker-compose，修改container的名字，数据目录修改为cmdata
- nginx改造为proxy，crontab改为cronjobs（但尚未取消docker in docker）

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



