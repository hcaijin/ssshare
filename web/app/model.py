#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from app.collections.sscol import SsCollection
from app.collections.newsscol import NewSsCollection


class SsshareModel(object):

    ltime = datetime.now() - timedelta(hours=1)

    def getSScount(self):
        return SsCollection.objects(uptime__gt=self.ltime).count()

    def getSSpage(self, page=1, per=100):
        return SsCollection.objects(uptime__gt=self.ltime) \
            .paginate(page=int(page), per_page=per)

    def getPage(self, page=1):
        return NewSsCollection.objects(status__gt=0).paginate(
            page=int(page), per_page=20)

    def test_removes(self):
        try:
            return NewSsCollection.objects.delete() + \
                SsCollection.objects.delete()
        except Exception as e:
            print(">" * 20, str(e))

    def getTopSS(self):
        return NewSsCollection.objects(content__not__contains='电信/联通/移动',
                                       status__gt=0).first_or_404()
