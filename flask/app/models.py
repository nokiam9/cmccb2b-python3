# -*- coding: utf-8 -*-

import datetime
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q

db = MongoEngine()  # 初始化数据库连接db


class BidNotice (db.Document):
    meta = {
        'collection': 'BidNotice',              # 设置collection名称，默认是model的名字
        'indexes': [                            # 设置index
            ("-published_date", "-timestamp"),  # 用于flask的列表排序
            "type_id",                          # 用于flask的列表选择
            "-timestamp",                       # 用于xunsearch的update index
        ],
    }
    _id = db.StringField()  # 必须增加，不然打开已存在的table时会报错
    nid = db.StringField()
    title = db.StringField()
    notice_type = db.StringField()
    source_ch = db.StringField()
    notice_url = db.StringField()
    notice_content = db.StringField()
    published_date = db.DateTimeField()
    timestamp = db.DateTimeField()
    reminded_time = db.DateTimeField()
    type_id = db.StringField()
    spider = db.StringField()
    attachment_urls = db.ListField(required=False)
    attachment_files = db.ListField(required=False)

    @classmethod
    def get_notice_content(cls, nid):
        return cls.objects(nid=nid).first().notice_content

    @classmethod
    def get_notice_pagination(cls, type_id, page_id, per_page):
        # 为了解决order by排序时内存溢出的问题，document的meta定义增加了index
        if type_id == '0' or type_id is None:
            return cls.objects(). \
                order_by("-published_date", "-timestamp"). \
                paginate(page=page_id, per_page=per_page)
        else:
            return cls.objects(type_id=type_id). \
                order_by("-published_date", "-timestamp"). \
                paginate(page=page_id, per_page=per_page)

    @classmethod
    def get_records_group_by_published_date(cls, days_before=-7):
        k, v = [], []
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # TimeZone 8
        for t0 in _get_days_list(now, days_before):
            t1 = t0 + datetime.timedelta(days=1)
            records = cls.objects(Q(published_date__lte=t1) & Q(published_date__gte=t0)).count()
            k.append(t0.strftime('%Y-%m-%d'))
            v.append(records)
        return k, v

    @classmethod
    def get_records_group_by_timestamp(cls, days_before=-7):
        k, v = [], []
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # TimeZone 8
        for t0 in _get_days_list(now, days_before):
            t1 = t0 + datetime.timedelta(days=1)
            records = cls.objects(Q(timestamp__lte=t1) & Q(timestamp__gte=t0)).count()
            k.append(t0.strftime('%Y-%m-%d'))
            v.append(records)
        return k, v

    @classmethod
    def get_records_group_by_source_ch(cls):
        k, v = [], []
        cursor = cls.objects().aggregate(
            {"$group": {"_id": "$source_ch", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        )
        for doc in cursor:
            k.append(doc['_id'])
            v.append(doc['count'])
        return k, v

    @classmethod
    def get_records_group_by_notice_type(cls):
        k, v = [], []
        cursor = cls.objects().aggregate(
            {"$group":
                {"_id": "$notice_type", "count":
                    {"$sum": 1}
                 }
             }
        )
        for doc in cursor:
            k.append(doc['_id'])
            v.append(doc['count'])
        return k, v


def _get_days_list(base_time, days_delta):
    """
    Function: 获得t0为基准的UTCTime日期序列数组，时间元素固定为0h0m0s，并按升序排列
        days_delta为正数时，［t0, t0+1day...］; 为负数时，［...,t0-1day,t0］
    """
    arr = []
    t0 = datetime.datetime(base_time.year, base_time.month, base_time.day)
    if days_delta > 0:
        for i in range(0, days_delta+1):
            t = t0 + datetime.timedelta(days=i)
            arr.append(t)
    else:
        for i in range(days_delta, 1):
            t = t0 + datetime.timedelta(days=i)
            arr.append(t)
    return arr

