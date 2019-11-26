#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.collections.sscol import SsCollection
from app.collections.newsscol import NewSsCollection


class SsshareModel(object):

    def getAllcount(self):
        return SsCollection.objects.count()

    def getAllpage(self, page=1, per=100):
        return SsCollection.objects.paginate(page=int(page), per_page=per)

    def getSScount(self):
        return SsCollection.objects(status__gte=0).count()

    def getSSpage(self, page=1, per=100):
        return SsCollection.objects(status__gte=0).paginate(page=int(page), per_page=per)

    def getPage(self, page=1):
        return NewSsCollection.objects(status__gt=0).paginate(page=int(page), per_page=20)

    def test_removes(self):
        try:
            return NewSsCollection.objects.delete() + \
                SsCollection.objects.delete()
        except Exception as e:
            print(">" * 20, str(e))

    def getTopSS(self):
        return NewSsCollection.objects(status__gt=0).first_or_404()
