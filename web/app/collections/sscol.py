#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from app import db


class SsCollection(db.Document):
    title = db.StringField(max_length=100, required=True, default="None title")
    url = db.StringField(max_length=100)
    hashcode = db.StringField(required=True, unique=True, default="")
    ssurl = db.StringField(required=True, default="")
    status = db.IntField(default=0)
    uptime = db.DateTimeField(default=datetime.now())

    meta = {
        'collection': 'ss_items',
    }

    @db.queryset_manager
    def new_sslist(doc_cls, queryset):
        return queryset.filter(uptime__gt=datetime.now())
