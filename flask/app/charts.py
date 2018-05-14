import random
import datetime
from pyecharts import Bar
from pyecharts_javascripthon.api import TRANSLATOR

from flask import render_template
from mongoengine.queryset.visitor import Q
from models import BidNotice


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def chart_view():
    _bar = _bar_chart()
    javascript_snippet = TRANSLATOR.translate(_bar.options)
    return render_template(
        "pyecharts.html",                                       # 自定义，位于templates/的模版文件
        chart_id=_bar.chart_id,                                 # 默认设置，
        host=REMOTE_HOST,                                       # 常量定义，存放js文件的url地址
        renderer=_bar.renderer,                                 # 默认设置，
        my_width="100%",                                        # 默认设置，定义图表的宽度
        my_height=600,                                          # 默认设置，定义图表的高度
        custom_function=javascript_snippet.function_snippet,    # 默认设置，保存图片的方法，似乎基于node.js
        options=javascript_snippet.option_snippet,              # 默认设置，
        script_list=_bar.get_js_dependencies(),                 # 默认设置，需要动态加载的js文件
    )


def _bar_chart():
    (x, y) = _get_records_group_by_day(-30)
    bar = Bar("招标公告发布趋势图", "From: cmccb2b")
    bar.use_theme('light')
    bar.add("发布日期", x, y, is_stack=False)        # 从Mongo读取的数据存放在这里
    # bar.print_echarts_options()                     # 该行只为了打印配置项，方便调试时使用
    return bar


def _get_records_group_by_day(days_before=-7):
    k, v = [], []
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # TimeZone 8
    t0 = datetime.datetime(now.year, now.month, now.day)
    for i in range(days_before, 0):
        t = t0 + datetime.timedelta(days=i)
        k.append(t.strftime('%Y-%m-%d'))
        v.append(_get_records_per_day(t))
    return k, v


def _get_records_per_day(t0):
    t1 = t0 + datetime.timedelta(days=1)
    return BidNotice.objects(Q(published_date__lte=t1) & Q(published_date__gte=t0)).count()



