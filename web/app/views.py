#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import threading
import math
from app import app
from flask import request, render_template, url_for, abort, redirect
from app.model import SsshareModel
from app.scheduler import saveItems
from apscheduler.schedulers.background import BackgroundScheduler


model = SsshareModel()
scheduler = BackgroundScheduler()


def startBackground():
    try:
        size = 20
        count = model.getSScount()
        print("=" * 20 + "have %d count items>" % count)
        if count > 0:
            for page in range(1, math.ceil(count/float(size)) + 1):
                print("=" * 20 + "page>", page)
                listss = model.getSSpage(page=page, per=size).items
                saveItems(listss)
    except Exception as e:
        print("=" * 20 + ">", "start backgroup cron error!")
        logging.exception(e)


@app.route('/all', methods=['GET'])
def allsslist():
    try:
        page = request.args.get('page', 1)
        count = model.getSScount()
        sslist = model.getSSpage(page=page, per=20)
        return render_template(
            'all.html',
            sslist=sslist,
            count=count
        )
    except Exception as e:
        logging.exception(e)
        abort(404)


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    try:
        page = request.args.get('page', 1)
        return render_template(
            'index.html',
            sslist=model.getPage(page),
        )
    except Exception as e:
        logging.exception(e)
        abort(404)


@app.route('/removes')
def removes():
    try:
        result = model.test_removes()
        if result > 0:
            print(">"*20, "Remove sucess!")
        else:
            print(">"*20, "Remove error!")
        return redirect(url_for('index'))
    except Exception as e:
        logging.exception("remove error:%s", str(e))
        abort(404)


@app.route('/setting')
def setting():
    try:
        topss = model.getTopSS()
        #  print("=" * 20 + ">", "setting show message:%s" % type(topss))
        if topss:
            with open('/etc/shadowsocks/config.json', 'w') as f:
                f.write(topss.config_json)
            return {'status': 0, 'info': 'sucess'}
        return {'status': 404, 'info': 'fails'}
    except Exception as e:
        logging.exception("setting error:%s", str(e))
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404


def start():
    print("=" * 20 + ">", "start add jobs")
    update_thread = threading.Thread(target=startBackground)
    scheduler.add_job(startBackground, trigger='cron', minute='*/20')
    update_thread.start()
    scheduler.start()
