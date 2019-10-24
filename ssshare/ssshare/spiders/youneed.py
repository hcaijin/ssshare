# -*- coding: utf-8 -*-
import scrapy
import re
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
            """
            # TODO: youneed.win/free-ssr/2 page url request
                //tbody/a[@class='post-page-numbers'][@href]")
            listhref = selector.xpath("//article[@id='post-box'] \
                                      //div[@class='page-links'] \
                                      //a[@class='post-page-numbers']/@href")
            for sub in listhref:
                yield scrapy.Request(url=sub, callback=parse_ss)
            """
            listss.update(map(lambda x: re.sub('\\s', '', x),
                              re.findall('ssr?://[a-zA-Z0-9_]+=*', str(text))))
            title = selector.xpath("//title/text()").get(default=self.name)
            return self.parse_items(listss, response.url, title)

    def parse_subscr(self, response):
        items = Util.decode(response.text).split('\n')
        return self.parse_items(items, response.url)

    # only support youneed.win/free-ss site
    def parse_free_ss(self, response):
        selector = Selector(response)
        title = selector.xpath("//title/text()").get(default=self.name)
        listtr = selector.xpath("//article[@id='post-box']//tbody/tr")
        return self.parse_items(listtr, response.url, title)

    def parse_items(self, items, url, title="SS or SSR 订阅源"):
        sssitem = SsshareItem()
        listss = list()
        for k, item in enumerate(set(items)):
            if isinstance(item, Selector):
                td = item.xpath(".//td/text()").getall()
                if len(td) > 3:
                    self.logger.debug('List ss: %s', str(td))
                    ssurl = 'ss://%s' % Util.encode(
                        '%s:%s@%s:%s' % (td[0], td[1], td[2], td[3]))
                    self.logger.debug('List ssurl: %s', ssurl)
                    listss.append(self.get_item(ssurl, url, title, k))
            else:
                if len(item) > 5:
                    self.logger.debug('List ssurl: %s', str(item))
                    listss.append(self.get_item(item, url, title, k))
        sssitem["listss"] = listss
        return sssitem

    def get_item(self, item, url, title, k):
        return {
            "title": " ".join([title, str(k)]),
            "url": url,
            "hashcode": Util.hashmd5(item),
            "ssurl": item
        }
