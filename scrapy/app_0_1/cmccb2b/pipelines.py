# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from scrapy.exceptions import DropItem


class Cmccb2bPipeline(object):
    """ Standard scrapy mongo pipeline, config by settings.py """
    # Default settings of config
    config = {
        'uri': 'mongodb://localhost:27017',
        'database': 'scrapy',
        'collection': 'items',
        'separate_collections': False,
        'unique_key': None,
        'stop_on_duplicate': 0,
    }

    def __init__(self):
        """ Construct """
        self.logger = logging.getLogger(__name__)
        self.collection = None
        self.stop_on_duplicate = 0
        self.duplicate_key_count = 0

    def open_spider(self, spider):
        """ Connect to MongoDB, get settings from spider.crawler """
        uri = spider.settings['MONGODB_URI']
        client = MongoClient(uri, connect=False)  # Notice: set connection for fork unsafe
        try:
            # Test with this ismaster command is cheap and does not require auth.
            client.admin.command('ismaster')
            self.logger.info(u'Connected to MongoDB, uri={0}.'.format(uri))
        except ConnectionFailure:
            self.logger.error(u'Connect MongoDB sever failed! uri={0}.'.format(uri))
            raise MongoConnectFailure   # TODO: unsupported raise failure

        database = client[spider.settings['MONGODB_DATABASE']]
        self.collection = database[spider.settings['MONGODB_COLLECTION']]
        self.logger.info(u'Locate collection successfully! db={0}, col={1}.'.format(
                spider.settings['MONGODB_DATABASE'],
                spider.settings['MONGODB_COLLECTION']))

        # Get collection and create unique index
        unique_key = spider.settings['MONGODB_UNIQUE_KEY']      # TODO: bug fix
        if unique_key:
            try:
                self.collection.create_index(unique_key, unique=True)
                self.logger.info(u'Create unique index for key {0}'.format(unique_key))
            except DuplicateKeyError:
                self.logger.error(u'Create unique index failed! key={0}'.format(unique_key))
                raise MongoIndexFailure   # TODO: unsupported raise failure

        # Get the duplicate on key option
        self.stop_on_duplicate = spider.settings.getint('MONGODB_STOP_ON_DUPLICATE')
        if self.stop_on_duplicate < 0:
            self.logger.error(u'Negative values are not allowed for MONGODB_STOP_ON_DUPLICATE.')
            raise SyntaxError     # TODO： exception unsupported

    def close_spider(self, spider):
        """ Close Spider， don't need to close mongo connect """
        self.logger.info(u'Spider will be closed, current_page={0}.'.format(spider.current_page))

    def process_item(self, item, spider):
        """ Insert item into mongo, stop when too many duplicate keys """
        try:
            self.collection.insert_one(dict(item))
            self.logger.debug(u'Stored one item in MongoDB.')
        except DuplicateKeyError:
            self.logger.debug(u'Duplicate key found. item={0}'.format(
                item.values()
            ))
            if self.stop_on_duplicate > 0:
                self.duplicate_key_count += 1
                if self.duplicate_key_count >= self.stop_on_duplicate:
                    # Notice: stop crawler when too many duplicate keys
                    spider.crawler.engine.close_spider(
                        spider,
                        'Number of duplicate key insertion exceeded'
                    )
                else:
                    raise DropItem
        return item

    def _from_settings(self, settings):
        # Set all regular options
        options = [
            ('uri', 'MONGODB_URI'),
            ('database', 'MONGODB_DATABASE'),
            ('collection', 'MONGODB_COLLECTION'),
            ('separate_collections', 'MONGODB_SEPARATE_COLLECTIONS'),
            ('unique_key', 'MONGODB_UNIQUE_KEY'),
            ('stop_on_duplicate', 'MONGODB_STOP_ON_DUPLICATE')
        ]

        # get config value from settings
        for k, v in options:
            if settings[v] and settings[v] != '':
                self.config[k] = settings[v]

        if not isinstance(self.config['stop_on_duplicate'], int):  # not number
            self.config['stop_on_duplicate'] = 0
            self.logger.warning(u"MONGODB_STOP_ON_DUPLICATE isn't type int, set default value with 0.")
        elif self.config['stop_on_duplicate'] < 0:
            self.logger.warning(u"MONGODB_STOP_ON_DUPLICATE < 0, set default value with 0.")

        v = self.config['unique_key']
        if not isinstance(v, str):
            if isinstance(v, list) or isinstance(v, tuple):
                for x in v:
                    if not isinstance(x, tuple) or len(x) != 2:
                        self.logger.warning(u"Value of MONGODB_UNIQUE_KEY with incorrect format，ignore this setting!")
                        del self.config['unique_key']
                        break
            else:
                self.logger.warning(u"Value of MONGODB_UNIQUE_KEY with incorrect format，ignore this setting!")
                del self.config['unique_key']

        return



