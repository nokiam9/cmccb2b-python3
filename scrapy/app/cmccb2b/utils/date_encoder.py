# -*- coding: utf-8 -*-
import json
import datetime


class DateEncoder(json.JSONEncoder):
    """
    解决json.dump不支持datetime的数据类型问题
    Usage: json.dumps(datalist, cls=CJsonEncoder)
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)