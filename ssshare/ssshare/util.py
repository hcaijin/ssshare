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
