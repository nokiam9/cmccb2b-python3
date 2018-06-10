# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine

db = MongoEngine()  # 初始化数据库连接db


class BidNotice (db.Document):
    meta = {
        'collection': 'BidNotice',              # 设置collection名称，默认是model的名字
        'indexes': [
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


