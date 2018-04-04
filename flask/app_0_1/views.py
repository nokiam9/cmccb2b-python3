# # -*- coding: utf-8 -*-

from flask import request, render_template, abort
from models import BidNotice, NoticeResult


# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中
def index():
    # return render_template('layout.html', rec_count=Todo.objects.count())
    return render_template('layout.html', rec_count=8888)   # TODO: fix it


def pageview(collection_name):
    config = {
        'bid_notice': BidNotice,
        'notice_result': NoticeResult,
    }
    page_num = request.args.get('page_id', default=1, type=int)

    try:
        document = config[collection_name]
    except KeyError:
        abort(status=404)               # TODO: set error handle

    # 为了解决order by排序时内存溢出的问题，安装脚本增加了按排序要求的索引
    todos_page = document.objects.order_by("-published_date", "-timestamp").paginate(page=page_num, per_page=10)

    return render_template('pagination.html', todos_page=todos_page)


def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"

