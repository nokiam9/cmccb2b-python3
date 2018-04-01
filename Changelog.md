### 开发记录 2018.04 ###
- 建立venv/的virtualenv，启动方式为`$ source venv/bin/activate`，退出方式为`$ deactivate`
- 新增`.gitignore`, 避免git引入开发过程文件
- 新增`workspace/`，用于一些临时测试和开发，通过后调整到正式文件
- 将`user_date/` 改名`data/`
- scrapy的logs改为docker volume方式，不再保存
- 修改`prestart.sh`，增加`-dev`参数，mongo补充启动docker-compose的override文件，以打开外部IP访问
- 修改`setup.sh`，将mongo/migrations的样本数据该用管道处理，
避免文件解压，并将目录设为只读，以便控制GitHub的数据量


### 遗留问题 ###
- `pip install scrpay`有bug，必须提前安装`incremental`(manage python project version )
- `pip install flask-mongoengine`有bug，必须提前安装nose, rednose, converage



