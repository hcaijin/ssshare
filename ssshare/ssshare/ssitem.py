#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from mongoengine import Document, StringField, DateTimeField


class SsItem(Document):
    title = StringField(max_length=100, required=True, default="None title")
    url = StringField(max_length=100)
    hashcode = StringField(required=True, unique=True, default="")
    ssurl = StringField(required=True, default="")
    uptime = DateTimeField(default=datetime.now())

    meta = {
        'collection': 'ss_items',
    }
