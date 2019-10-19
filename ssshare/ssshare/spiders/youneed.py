# -*- coding: utf-8 -*-
import scrapy
import base64
from scrapy.selector import Selector
from ssshare.items import SsshareItem

class YouneedSpider(scrapy.Spider):
    name = 'youneed'
    allowed_domains = ['youneed.win']
    start_urls = ['http://youneed.win/free-ss']

    def parse(self, response):
        self.logger.info('A response from %s', response.url)
        selector = Selector(response)
        title = selector.xpath("//title/text()").get(default=self.name)
        ssitem = SsshareItem()
        listItem = list()
        for tr in selector.xpath("//article[@id='post-box']//tbody/tr"):
            td = tr.xpath(".//td/text()").getall()
            self.logger.info('List ss: %s', str(td))
            encodess = 'ss://%s' % str(base64.urlsafe_b64encode(
                bytes('%s:%s@%s:%s' % (td[0], td[1], td[2], td[3]), 'utf-8')))
            self.logger.info('List ssurl: %s', encodess)
            item = {
                "server": td[0],
                "port": td[1],
                "passwd": td[2],
                "method": td[3],
                "uptime": td[4],
                "countries": td[5],
                "ssurl": encodess
            }
            listItem.append(item)
        ssitem["title"] = title
        ssitem["listss"] = listItem
        return ssitem
