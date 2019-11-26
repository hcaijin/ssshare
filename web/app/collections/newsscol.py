#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db


class NewSsCollection(db.Document):

    title = db.StringField(max_length=100, required=True, default="None title")
    url = db.StringField(max_length=100)
    hashcode = db.StringField(required=True, unique=True, default="")
    ssurl = db.StringField(required=True, default="")
    config_json = db.StringField()
    server = db.StringField()
    server_port = db.IntField()
    ssr_protocol = db.StringField()
    method = db.StringField()
    obfs = db.StringField()
    password = db.StringField()
    protocol = db.StringField()
    obfsparam = db.StringField()
    protoparam = db.StringField()
    udpport = db.StringField()
    uot = db.StringField()
    status = db.IntField()
    content = db.StringField()
    group = db.StringField()
    remarks = db.StringField()
    typename = db.IntField()

    meta = {
        'collection': 'new_ss_items',
        'ordering': ['+status']
    }
