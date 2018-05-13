import random
import datetime
from pyecharts import Scatter3D, Bar
from pyecharts_javascripthon.api import TRANSLATOR

from flask import render_template
from mongoengine.queryset.visitor import Q
from models import BidNotice


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def chart_view():
    _bar = bar_chart()
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


def bar_chart():
    k, v = get_week_list()
    bar = Bar("公告信息发布趋势图", "From: cmccb2b")
    bar.use_theme('light')
    bar.add("日期", k, v)         # 从Mongo读取的数据存放在这里
    bar.print_echarts_options()  # 该行只为了打印配置项，方便调试时使用
    return bar


def get_week_list():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    week_key = []
    week_value = []
    for i in range(-30, 1):
        t = now + datetime.timedelta(hours=24*i)
        t0 = datetime.datetime(t.year, t.month, t.day)
        t1 = t0 + datetime.timedelta(hours=24)
        r = get_records_daily(t0, t1)
        week_key.append(t.strftime('%Y-%m-%d'))
        week_value.append(r)
    return week_key, week_value


def get_records_daily(t0, t1):
    return BidNotice.objects(Q(published_date__lte=t1) & Q(published_date__gte=t0)).count()


def chart_view01():
    s3d = scatter3d()
    return render_template(
        "pyecharts01.html",
        myechart=s3d.render_embed(),
        host=REMOTE_HOST,
        script_list=s3d.get_js_dependencies(),
    )


def scatter3d():
    data = [generate_3d_random_point() for _ in range(80)]
    range_color = [
        "#313695",
        "#4575b4",
        "#74add1",
        "#abd9e9",
        "#e0f3f8",
        "#fee090",
        "#fdae61",
        "#f46d43",
        "#d73027",
        "#a50026",
    ]
    scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    return scatter3D


def generate_3d_random_point():
    return [
        random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
    ]


