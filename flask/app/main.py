# -*- coding: utf-8 -*-

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from models import db
import views
import charts


# 初始化app，原型在flask，并从settings.py中提取自定义的类属性，包括MongoDB配置，debug配置等
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config.from_pyfile(filename='settings.py')

# 连接flask和mongoengine，注意db在models.py中初始化，参数设置已经从app.config中加载
db.init_app(app)

# 所有route的定义，采用add_url_rule()，而不是@route("/")的修饰符方式，便于集中管理路由信息
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/index.html', view_func=views.index)
app.add_url_rule('/hello', view_func=views.hello)
app.add_url_rule('/content/<string:nid>', view_func=views.content_view)
app.add_url_rule('/notice/pagination/<string:type_id>', view_func=views.notice_page_view)
app.add_url_rule('/chart01', view_func=charts.chart_view01)
app.add_url_rule('/chart02', view_func=charts.chart_view02)
app.add_url_rule('/chart03', view_func=charts.chart_view03)
app.add_url_rule('/chart04', view_func=charts.chart_view04)

# 仅用于flask Debug，生产环境应取消
toolbar = DebugToolbarExtension(app)    # 该扩展要求app必须设置SECRET_KEY，已包含在settings.py中
app.debug = False

if __name__ == "__main__":

    # app.run()启动flask自带web server
    # 嵌入uWSGI后app.run()不会执行，而是引用该py的app变量，uWSGI的设置在uwsgi.ini中，port也会修改
    app.run(host='0.0.0.0', debug=False, port=3000)






