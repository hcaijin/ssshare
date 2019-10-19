# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from ssshare.items import SsshareItem

class SssharePipeline(object):
    collection_name = 'ss_items'
    logger = logging.getLogger(__name__)

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'ssshare_db')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, SsshareItem):
            dicItem = dict(item)
            self.logger.info('Save to mongodb item: [%s]', str(dicItem))
            try:
                self.db[self.collection_name].insert_one(dicItem)
            except Exception as e:
                self.logger.error('Save to mongodb error:%s', str(e))
        return item
