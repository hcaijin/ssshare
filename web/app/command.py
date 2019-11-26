#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import logging
from flask.cli import with_appcontext
from app.model import SsshareModel


model = SsshareModel()


@click.command("init-ss")
@with_appcontext
def init_ss():
    try:
        topss = model.getTopSS()
        #  print("=" * 20 + ">", "setting show message:%s" % type(topss))
        if topss:
            with open('/etc/shadowsocks/config.json', 'w') as f:
                f.write(topss.config_json)
            return 0
        return 500
    except Exception as e:
        logging.exception("init-ss error:%s", str(e))
