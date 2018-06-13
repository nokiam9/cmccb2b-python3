# -*- coding: utf-8 -*-

MONGODB_SETTINGS = {'DB': 'cmccb2b',
                    'host': 'mongo',  # 0.0.0.0 for local | mongo for docker
                    'port': 27017,
                    'connect': False  # set for pymongo bug fix
                    }
SECRET_KEY = "flask+mongoengine=<3"     # flask-debug必须设置该参数，为session提供加密处理

# DEBUG_TB_INTERCEPT_REDIRECTS = False
