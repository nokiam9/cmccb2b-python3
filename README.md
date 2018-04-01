### cmccb2b Package Based on Python3.6 ###

#### 开发记录 ####
- 建立venv/的virtualenv，启动方式为`$ source venv/bin/activate`，退出方式为`$ deactivate`
- 修改`prestart.sh`的启动方式，默认为runtime方式，开发时`-dev`放开mongo的端口限制
- `pip install scrpay`有bug，必须提前安装`incremental`(manage python project version )
- `pip install flask-mongoengine`有bug，必须提前安装nose, rednose, converage


