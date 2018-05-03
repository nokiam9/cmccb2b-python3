# -*- coding: utf-8 -*-

from flask import Flask
from models import db
import views

# 初始化app，原型在flask，并从app.config中读取自定义的参数
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config.from_pyfile(filename='settings.py')

# 连接flask和mongoengine，注意db在models.py中初始化，参数设置在settings.py中（已提前加载）
db.init_app(app)

# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将所有视图隐藏在views.py中
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/index.html', view_func=views.index)
app.add_url_rule('/hello', view_func=views.hello)
app.add_url_rule('/context/<string:notice_id>', view_func=views.context_view)
app.add_url_rule('/notice/pagination/<string:type_id>', view_func=views.notice_page_view)


if __name__ == "__main__":

    # app.run()启动flask自带web server
    # 嵌入uWSGI后app.run()不会执行，而是引用该py的app变量，uWSGI的设置在uwsgi.ini中，port也会修改
    app.run(host='0.0.0.0', debug=False, port=3000)






