#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import importlib
import json
import sys
import time
import xml.etree.ElementTree as ET

from flask import Flask, make_response, request

from . import app, dispatcher

importlib.reload(sys)  # 不加这部分处理中文还是会出问题

@app.route('/')  # 默认网址
def index():
    return 'Index Page'

@app.route("/data")
@app.route("/MP_verify_7QJH9uUdXgv284uQ.txt")
def get_data():
    print("hello data")
    return app.send_static_file("MP_verify_7QJH9uUdXgv284uQ.txt")

@app.route('/wx', methods=['GET', 'POST'])
def wechat_auth():
    '''
    微信请求的处理函数，GET方法用于认证，POST方法取得微信转发的数据
    '''
    if request.method == 'GET':
        token = 'kundy0808'

        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')

        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s.encode('utf-8')).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        disp = dispatcher.MsgDispatcher(rec)
        data = disp.dispatch()

        with open("./debug.log", "a") as file:
            file.write(data)
            file.close()

        response = make_response(data)
        response.content_type = 'application/xml'
        return response
