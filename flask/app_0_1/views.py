# # -*- coding: utf-8 -*-

from flask import request, render_template, abort
from models import BidNotice, NoticeResult, SingleSourceProcurement

collections = {
    'bid_notice': (u'招标公告', BidNotice),
    'notice_result': (u'中标公示', NoticeResult),
    'single_source_procurement': (u'单一来源采购', SingleSourceProcurement),
}


# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中
def index():
    return render_template('layout.html')


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

