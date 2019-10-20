# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from pymongo import MongoClient
from ssshare.items import SsshareItem
from pymongo.errors import ConnectionFailure


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
        try:
            self.client = MongoClient(self.mongo_uri)
            db = self.client[self.mongo_db]
            self.col = db[self.collection_name]
            self.col.create_index([("hashcode")], unique=True)
        except ConnectionFailure:
            self.logger.error("Mongodb connect fail")
        except Exception as e:
            self.logger.error('Open mongodb error:%s', str(e))

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, SsshareItem):
            self.logger.debug('Show spider item: [%s]', str(item))
            try:
                savess = list()
                listss = item['listss']
                for ss in listss:
                    res = self.col.find_one({"hashcode": ss['hashcode']})
                    if res is None:
                        savess.append(ss)
                # Only insert not in collection
                if len(savess) > 0:
                    self.logger.info(
                        'Save new list ss to mongodb has [%d] count',
                        len(savess))
                    self.logger.debug('Save to mongodb: [%s]', str(savess))
                    self.col.insert_many(savess)
            except Exception as e:
                self.logger.error('Save to mongodb error:%s', str(e))
        return item
