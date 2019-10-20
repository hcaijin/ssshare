# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from ssshare.items import SsshareItem
from ssshare.url_config import URLS, SUBSCRIPTIONS, CUSTOMURLS
from ssshare.util import Util


class YouneedSpider(scrapy.Spider):

    name = 'youneed'
    allowed_domains = ['youneed.win']
    urls = list(set(URLS))
    subscriptions = list(set(SUBSCRIPTIONS))
    customurls = list(set(CUSTOMURLS))

    def start_requests(self):
        for curl in self.customurls:
            self.logger.info('Start request from custom url: %s', curl)
            yield scrapy.Request(url=curl, callback=self.parse_url)
        for url in self.urls:
            self.logger.info('Start request from url: %s', url)
            yield scrapy.Request(url=url, callback=self.parse_ss)
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
            return self.parse_item(selector, listss)

    def parse_url(self, response):
        selector = Selector(response)
        listtr = selector.xpath("//article[@id='post-box']//tbody/tr")
        return self.parse_item(selector, listtr)

    def parse_item(self, selector, items):
        title = selector.xpath("//title/text()").get(default=self.name)
        ssitem = SsshareItem()
        listss = list()
        if type(items) is set:
            for i, ss in enumerate(items):
                listss.append({
                    "title": ' '.join([title, str(i)]),
                    "hashcode": Util.hashmd5(ss),
                    "ssurl": ss
                })
        else:
            k = 0
            for ss in items:
                td = ss.xpath(".//td/text()").getall()
                self.logger.debug('List ss: %s', str(td))
                ssurl = 'ss://%s' % Util.encode('%s:%s@%s:%s' %
                                                (td[0], td[1], td[2], td[3]))
                self.logger.debug('List ssurl: %s', ssurl)
                listss.append({
                    "title": ' '.join([title, str(k)]),
                    "hashcode": Util.hashmd5(ssurl),
                    "ssurl": ssurl
                })
                k = k + 1
        ssitem["listss"] = listss
        return ssitem
