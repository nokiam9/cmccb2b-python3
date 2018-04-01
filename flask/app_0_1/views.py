# # -*- coding: utf-8 -*-

from flask import request, render_template
from models import Todo


# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中
def index():
    return render_template('layout.html', rec_count=Todo.objects.count())


def pageview():
    page_num = request.args.get('page_id', default=1, type=int)

    # 为了解决order by排序时内存溢出的问题，安装脚本增加了按排序要求的索引
    todos_page = Todo.objects.order_by("-published_date", "-timestamp").paginate(page=page_num, per_page=10)

    return render_template('pagination.html', todos_page=todos_page)


def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"