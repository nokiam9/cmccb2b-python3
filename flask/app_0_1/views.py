# # -*- coding: utf-8 -*-

from flask import request, render_template, abort
from models import BidNotice, NoticeResult, SingleSourceProcurement

collections = {
    'bid_notice': (u'招标公告', BidNotice),
    'notice_result': (u'中标公示', NoticeResult),
    'single_source_procurement': (u'单一来源采购', SingleSourceProcurement),
}
NOTICE_TYPE_CONFIG = {
    '0': '全部招标公告',
    '1': '单一来源采购公告',
    '2': '采购公告',
    '3': '中标公示',
    '7': '资格预审公告',
    '8': '供应商信息收集',
}
PAGE_SIZE = 10


# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中
def index():
    # return render_template('layout.html')
    return render_template('index.html')


def page_view(collection_name):
    page_num = request.args.get('page_id', default=1, type=int)

    try:
        title = collections[collection_name][0]
        document = collections[collection_name][1]
    except KeyError:
        abort(status=404)

    # 为了解决order by排序时内存溢出的问题，document的meta定义增加了index
    todos_page = document.objects.\
        order_by("-published_date", "-timestamp").\
        paginate(page=page_num, per_page=10)

    return render_template('pagination.html',
                           todos_page=todos_page,
                           collection_name=collection_name,
                           title=title)


def context_view(notice_id):
    context = BidNotice.objects(id=notice_id).first().notice_context
    if not context:
        return notice_id
        abort(status=404)
    else:
        return context


def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"


def notice_page_view(type_id):
    """  View of /notice/pagination/[012378]/?page_id=1 """
    page_id = request.args.get('page_id', default=1, type=int)

    try:
        title = NOTICE_TYPE_CONFIG[type_id]
    except KeyError:
        abort(status=402)

    # 为了解决order by排序时内存溢出的问题，document的meta定义增加了index
    if type_id == '0':
        todos_page = BidNotice.objects().\
            order_by("-published_date", "-timestamp").\
            paginate(page=page_id, per_page=PAGE_SIZE)
    else:
        todos_page = BidNotice.objects(type_id=type_id).\
            order_by("-published_date", "-timestamp").\
            paginate(page=page_id, per_page=PAGE_SIZE)

    return render_template('pagination.html',
                           todos_page=todos_page,
                           type_id=type_id,
                           title=title)


