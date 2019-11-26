#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import json
import urllib
from app.speedtest import test_speed
from app.util import Util
from app.collections.sscol import SsCollection
from app.collections.newsscol import NewSsCollection

logger = logging.getLogger(__name__)


def saveItems(sslist):
    print("=" * 20, "save items fun")
    saveItems = _getItems(sslist)
    count = len(saveItems)
    logger.info('Save count %d ss items', count)
    if count > 0:
        try:
            NewSsCollection.objects.insert(saveItems)
        except Exception as e:
            logger.error('Save new ss items fails:%s', str(e))


def _parse(url, remark):
    server = dict()
    reg = re.search('(^ssr?://)(.*)', url)
    if reg is not None:
        head, sstr = reg.groups()
        if len(sstr) > 0:
            if head == 'ss://':
                if '#' in sstr:
                    sstr, remarks = sstr.split('#')[:2]
                    server['remarks'] = urllib.parse.unquote(remarks)
                else:
                    server['remarks'] = remark
                ss = Util.decode(sstr).split('@', maxsplit=1)
                if len(ss) == 2:
                    server['server'], server['server_port'] = ss[1].split(
                        ':', maxsplit=1)
                    server['method'], server['password'] = ss[0].split(
                        ':', maxsplit=1)
                server['typename'] = 1
            elif head == 'ssr://':
                ssr = Util.decode(sstr).split('/?', maxsplit=1)
                [
                    server['server'],
                    server['server_port'],
                    server['ssr_protocol'],
                    server['method'],
                    server['obfs'],
                    passwd_encode,
                ] = ssr[0].split(':', maxsplit=5)
                server['password'] = Util.decode(passwd_encode)
                server['remarks'] = remark
                if len(ssr) > 1:
                    for p in ssr[1].split('&'):
                        key, val = p.split('=', maxsplit=1)
                        server[key] = Util.decode(val)
                if server['ssr_protocol'] != 'origin' and \
                        server['obfs'] != 'plain':
                    server['remarks'] += ' SSR'
                server['typename'] = 2
    return server


def _formatJson(server):
    for k in ['server', 'server_port', 'password']:
        if k not in server:
            print(">" * 20, "format json error:%s" % str(server))
            return None
    config_json = {
        "server": server['server'],
        "server_ipv6": "::",
        "server_port": int(server['server_port']),
        "local_address": "127.0.0.1",
        "local_port": 1080,
        "password": server['password'],
        "group": "ssshare group"
    }
    if 'ssr_protocol' in server:
        server['protocol'] = server['ssr_protocol']
    for key in ['obfs', 'method', 'protocol', 'obfsparam', 'protoparam',
                'udpport', 'uot']:
        if key in server:
            config_json[key] = server.get(key)
    return json.dumps(config_json, ensure_ascii=False, indent=2)


def _getItems(listss):
    ucount = 0
    saveItems = list()
    #  print("=" * 20, "listss len:%s" % len(listss))
    for ss in listss:
        server = _parse(ss.ssurl, ss.title)
        cjson = _formatJson(server)
        if cjson is None:
            continue
        server['title'] = ss.title
        server['url'] = ss.url
        server['hashcode'] = ss.hashcode
        server['ssurl'] = ss.ssurl
        server['config_json'] = cjson
        server['status'], server['content'] = test_speed(cjson)
        ssobj = dict2obj(server)
        if isinstance(ssobj, NewSsCollection):
            try:
                SsCollection.objects(hashcode=ssobj.hashcode).update_one(status=ssobj.status)
            except Exception as es:
                logger.error("Update ss collection status error:%s", str(es))
            try:
                oness = NewSsCollection.objects(hashcode=ss.hashcode).first()
            except Exception as e:
                oness = None
                logger.error("Get one ss error:%s", str(e))
            if oness is None:
                saveItems.append(ssobj)
            else:
                try:
                    NewSsCollection.objects(hashcode=oness.hashcode) \
                        .update_one(status=ssobj.status, content=ssobj.content)
                    ucount += 1
                except Exception as ex:
                    logger.error("update hashcode equat %s, error:%s",
                                 oness.hashcode, str(ex))
    logger.info('Update count %d ss items', ucount)
    return saveItems


def dict2obj(d):
    try:
        d = dict(d)
    except (TypeError, ValueError):
        return d
    obj = NewSsCollection()
    for k, v in d.items():
        obj[k] = v
    return obj
