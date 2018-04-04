# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, OperationFailure, InvalidURI
from scrapy.exceptions import DropItem


class Cmccb2bPipeline(object):
    """ Standard scrapy mongo pipeline, config by settings.py """
    def __init__(self):
        """ Construct """
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.collection = None
        self.stop_on_duplicate = 0
        self.duplicate_key_count = 0

    def open_spider(self, spider):
        """ Connect to MongoDB, get settings from spider.crawler """
        self._get_config(spider)

        uri = self.config['uri']
        client = MongoClient(uri, connect=False)  # Notice: set connection for fork unsafe
        try:
            # Test with this ismaster command is cheap and does not require auth.
            client.admin.command('ismaster')
            self.logger.info(u'Connected to MongoDB, uri={0}.'.format(uri))
        except (InvalidURI, ConnectionFailure):
            self.logger.error(u'Connect MongoDB sever failed and abort now! uri={0}.'.format(uri))
            raise MongoConnectFailure   # TODO: unsupported raise exception

        database = client[self.config['database']]
        self.collection = database[self.config['collection']]
        self.logger.info(u'Locate collection successfully! db={0}, col={1}.'.format(
                self.config['database'],
                self.config['collection']))

        # Get collection and create unique index
        unique_key = self.config['unique_key']
        if unique_key != '':      # if data format error, just ignore it
            try:
                self.collection.create_index(unique_key, unique=True)
                self.logger.info(u'Create unique index with key={0}'.format(unique_key))
            except (DuplicateKeyError, OperationFailure):
                self.logger.error(u'Failed to create unique index and abort now! key={0}'.format(unique_key))
                raise MongoIndexFailure   # TODO: unsupported raise exception
        else:
            self.logger.info(u'Pipeline mongo without unique index...')

        # Get the duplicate on key option
        self.stop_on_duplicate = self.config['stop_on_duplicate']   # if data error, reset with 0
        self.logger.info(u'Set stop_on_duplicate with {0}.'.format(self.stop_on_duplicate))

    def close_spider(self, spider):
        """ Close Spider， no need to close mongo connect """
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
                    spider.crawler.engine.close_spider(spider, 'Number of duplicate key insertion exceeded')
                raise DropItem
        return item

    def _get_config(self, spider):
        # get config value from settings
        self.config['uri'] = spider.settings.get('MONGODB_URI', default='mongodb://localhost:12017')
        self.config['database'] = spider.settings.get('MONGODB_DATABASE', default='scrapy')
        self.config['collection'] = spider.settings.get('MONGODB_COLLECTION', default='items')
        self.config['unique_key'] = spider.settings.get('MONGODB_UNIQUE_KEY', default='')
        self.config['stop_on_duplicate'] = spider.settings.getint('MONGODB_STOP_ON_DUPLICATE', default=0)

        # if set SEPARATE_COLLECTIONS, set collection with spider name, and ignore MONGODB_COLLECTION
        if spider.settings.getbool('MONGODB_SEPARATE_COLLECTIONS', default=False):
            if self.config['collection'] != spider.name:
                self.config['collection'] = spider.name
                self.logger.warning(u"Ignore MONGODB_COLLECTION for SEPARATE_COLLECTIONS=True！")

        v = self.config['stop_on_duplicate']
        if not isinstance(v, int) or v < 0:
            self.config['stop_on_duplicate'] = 0
            self.logger.warning(u"MONGODB_STOP_ON_DUPLICATE format error, set default value with 0.")

        v = self.config['unique_key']
        if not isinstance(v, str):
            if isinstance(v, list):
                for x in v:
                    if not isinstance(x, tuple) or len(x) != 2:
                        self.logger.warning(u"Value of MONGODB_UNIQUE_KEY with incorrect format，ignore this setting!")
                        self.config['unique_key'] = ''
                        break
            else:
                self.logger.warning(u"Value of MONGODB_UNIQUE_KEY with incorrect format，ignore this setting!")
                self.config['unique_key'] = ''
        return




