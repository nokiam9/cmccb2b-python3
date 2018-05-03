# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine

db = MongoEngine()  # 初始化数据库连接db


class BidNotice (db.Document):
    meta = {
        'collection': 'BidNotice',     # set collection name here!
        'indexes': [("-published_date", "-timestamp")],
    }
    _id = db.StringField()  # 必须增加，不然打开已存在的table时会报错
    id = db.StringField()
    title = db.StringField()
    notice_type = db.StringField()
    source_ch = db.StringField()
    notice_url = db.StringField()
    notice_context = db.StringField()
    published_date = db.DateTimeField()
    timestamp = db.DateTimeField()
    reminded_time = db.DateTimeField()
    type_id = db.StringField()


