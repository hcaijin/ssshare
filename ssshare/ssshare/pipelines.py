# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from ssshare.items import SsshareItem
from mongoengine import connect, disconnect
from ssshare.ssitem import SsItem


class SssharePipeline(object):
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
            connect(self.mongo_db, host=self.mongo_uri)
        except Exception as e:
            self.logger.error('Open mongodb error:%s', str(e))

    def close_spider(self, spider):
        disconnect(self.mongo_db)

    def process_item(self, item, spider):
        if isinstance(item, SsshareItem):
            update_count = 0
            savess = list()
            for ss in item['listss']:
                try:
                    res = SsItem.objects(hashcode=ss['hashcode']).first()
                except Exception as e:
                    self.logger.error("Find hashcode(%s) error:%s", ss['hashcode'], str(e))
                    continue
                if res is None:
                    # Only insert not in collection
                    savess.append(self.dict2obj(ss))
                else:
                    try:
                        SsItem.objects(hashcode=res.hashcode, status__lt=0).update_one(status=0)
                        update_count += 1
                    except Exception as e:
                        self.logger.error("Update hashcode(%s) error:%s", res.hashcode, str(e))
                        continue
            self.logger.info('Update ss to mongodb has [%d] count', update_count)
            count = len(savess)
            if count > 0:
                try:
                    SsItem.objects.insert(savess)
                except Exception as e:
                    self.logger.error('Save to mongodb error:%s', str(e))
            self.logger.info('Save new ss to mongodb has [%d] count', count)

    def dict2obj(self, d):
        try:
            d = dict(d)
        except (TypeError, ValueError):
            return d
        obj = SsItem()
        for k, v in d.items():
            obj[k] = v
        return obj
