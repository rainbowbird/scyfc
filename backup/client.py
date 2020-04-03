#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpc.client

proxy = xmlrpc.client.ServerProxy('http://localhost:9000')

print(proxy.get_access_token())
