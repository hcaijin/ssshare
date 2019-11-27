# -*- coding: utf-8 -*-
import scrapy
import re
import urllib
from scrapy.selector import Selector
from ssshare.items import SsshareItem
from ssshare.url_config import URLS, SUBSCRIPTIONS
from ssshare.util import Util


class YouneedSpider(scrapy.Spider):

    name = 'youneed'
    allowed_domains = ['youneed.win']
    urls = list(set(URLS))
    subscriptions = list(set(SUBSCRIPTIONS))

    def start_requests(self):
        for url in self.urls:
            self.logger.info('Start request from url: %s', url)
            callbackfun = self.parse_ss
            if url == 'https://www.youneed.win/free-ss':
                callbackfun = self.parse_free_ss
            yield scrapy.Request(url=url, callback=callbackfun)
        for sub in self.subscriptions:
            self.logger.info('Start request from subscriptions: %s', sub)
            yield scrapy.Request(url=sub, callback=self.parse_subscr)

    def parse_ss(self, response):
        selector = Selector(response)
        listss = set()
        text = selector.getall()
        if text:
            if response.url == 'https://www.youneed.win/free-ssr':
                listhref = selector.xpath(
                    "//a[@class='post-page-numbers']/@href").getall()
                for sub in listhref:
                    yield scrapy.Request(url=sub, callback=self.parse_ss)
            listss.update(map(lambda x: re.sub('\\s', '', x),
                              re.findall('ssr?://[a-zA-Z0-9_]+=*', str(text))))
            title = selector.xpath("//title/text()").get(default=self.name)
            yield self.parse_items(listss, response.url, title)

    def parse_subscr(self, response):
        items = Util.decode(response.text).split('\n')
        yield self.parse_items(items, response.url)

    # only support youneed.win/free-ss site
    def parse_free_ss(self, response):
        selector = Selector(response)
        title = selector.xpath("//title/text()").get(default=self.name)
        listtr = selector.xpath("//article[@id='post-box']//tbody/tr")
        yield self.parse_items(listtr, response.url, title)

    def parse_items(self, items, url, title="订阅源 -"):
        sssitem = SsshareItem()
        listss = list()
        for k, item in enumerate(set(items)):
            jtitle = " ".join([title, str(k)])
            if isinstance(item, Selector):
                td = item.xpath(".//td/text()").getall()
                if len(td) > 3:
                    self.logger.debug('List ss: %s', str(td))
                    ssheader = '{method}:{password}@{hostname}:{port}'.format(
                        method=td[3],
                        password=td[2],
                        hostname=td[0],
                        port=td[1],
                    )
                    ssurl = 'ss://{}#{}'.format(str(Util.encode(ssheader)),
                                                urllib.parse.quote(jtitle))
                    listss.append(self.get_item(ssurl, url, jtitle))
            else:
                if len(item) > 5:
                    listss.append(self.get_item(item, url, jtitle))
        sssitem["listss"] = listss
        return sssitem

    def get_item(self, item, url, title):
        self.logger.debug('List ssurl: %s', str(item))
        return {
            "title": title,
            "url": url,
            "hashcode": Util.hashmd5(item.split('#', maxsplit=1)[0]),
            "ssurl": item,
        }
