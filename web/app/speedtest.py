#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import threading
import random
from app import ss_local


# url = cip.cc | ping.pe | myip.ipip.net | ip.cn
def test_connection(
        url='http://myip.ipip.net',
        headers={'User-Agent': 'curl/7.21.3 (i686-pc-linux-gnu) '
                 'libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'},
        proxies=None, port=1080, timeout=10):
    if not proxies:
        proxies = {'http': 'socks5://localhost:{}'.format(port), 'https':
                   'socks5://localhost:{}'.format(port)}
    ok = -1
    content = ''
    try:
        start = time.time()
        respond = requests.get(url, headers=headers, proxies=proxies,
                               timeout=timeout)
        if respond.ok:
            ok = (time.time() - start) * 1000
            content = respond.text
        else:
            ok = respond.ok
            content = respond.text
    except Exception as e:
        print(e)
        content = repr(e)
    return int(ok), content


def test_socks_server(dictionary=None, str_json=None, port=None):
    if not port:
        port = random.randint(12000, 13000)
    try:
        try:
            loop, tcps, udps = ss_local.main(
                dictionary=dictionary, str_json=str_json, port=port)
        except Exception as e:
            print(e)
            return -1, 'SSR start failed'
        try:
            t = threading.Thread(target=loop.run)
            t.start()
            time.sleep(3)
            conn, content = test_connection(port=port)
            loop.stop()
            t.join()
            tcps.close(next_tick=True)
            udps.close(next_tick=True)
            time.sleep(1)
            return conn, content
        except Exception as e:
            print(e)
            return -2, 'Thread or Connection to website failed'
    except SystemExit as e:
        return e.code - 10, 'Unknown failure'


def test_speed(str_json):
    result, info = test_socks_server(str_json=str_json)
    print('>' * 10, 'Result:', result)
    if result >= 0:
        print('>' * 20, 'Connect sucess.')
    elif result == -1:
        print('>' * 20, 'Connect except!')
    else:
        print('>' * 20, 'Other error!')
    return result, info


if __name__ == '__main__':
    print(test_connection())
