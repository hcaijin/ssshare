#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import base64


class Util(object):

    def hashmd5(s):
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def encode(string):
        return base64.urlsafe_b64encode(
            bytes(str(string), 'utf-8')).decode('utf-8').replace('=', '')

    def decode(string):
        try:
            return str(
                base64.urlsafe_b64decode(
                    bytes(
                        string.strip('/') +
                        (4 - len(string.strip('/')) % 4) * '=' + '====',
                        'utf-8')), 'utf-8')
        except Exception as e:
            raise Exception(e, string)
