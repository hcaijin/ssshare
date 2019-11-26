#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('config.default_setting')
app.config.from_envvar('FLASK_SETTINGS', silent=True)
db = MongoEngine(app)
from app import views
views.start()
