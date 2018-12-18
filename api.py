#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import importlib
import time
import hashlib
import json
import xml.etree.ElementTree as ET
from flask import Flask, request, make_response
from dispatcher import *

importlib.reload(sys)  # 不加这部分处理中文还是会出问题

app = Flask(__name__)
app.debug = True


@app.route('/')  # 默认网址
def index():
    return 'Index Page'


@app.route('/wx', methods=['GET', 'POST'])
def wechat_auth():  
    '''
    处理微信请求的处理函数，get方法用于认证，post方法取得微信转发的数据
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
        rec = request.stream.read()  # 接收消息
        dispatcher = MsgDispatcher(rec)
        data = dispatcher.dispatch()
        with open("./debug.log", "a") as file:
            file.write(data)
            file.close()
        response = make_response(data)
        response.content_type = 'application/xml'
        return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

