# # -*- coding: utf-8 -*-

from flask import request, render_template, abort
from models import *

NOTICE_TYPE_CONFIG = {
    '0': '全部招标公告',
    '1': '单一来源采购公告',
    '2': '采购公告',
    '7': '中标结果公示',
    '3': '资格预审公告',
    '8': '供应商信息收集',
}
PAGE_SIZE = 10


# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中
def index():
    return render_template('index.html')


def content_view(nid):
    content = get_content(nid)
    if not content:
        return nid
        abort(status=404)
    else:
        return content


def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"


def notice_page_view(type_id):
    """  View of /notice/pagination/[012378]/?page_id=1 """
    try:
        title = NOTICE_TYPE_CONFIG[type_id]
    except KeyError:
        abort(status=406)   # Unacceptable url para

    todos_page = get_notice_pagination(
        type_id=type_id,
        page_id=request.args.get('page_id', default=1, type=int),
        per_page=PAGE_SIZE
    )
    return render_template('pagination.html',
                           todos_page=todos_page,
                           type_id=type_id,
                           title=title)


