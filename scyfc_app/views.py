#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import importlib
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from flask import Flask, make_response, redirect, render_template, request

from . import app, dispatcher

importlib.reload(sys)  # 不加这部分处理中文还是会出问题


APPID = "wxb0bb415e8ca0d547"
APPSECRET = "6c40dd3dc217138b77189ce08c748d1c"

@app.route('/')  # 默认网址
def index():
    return '<h1>Index Page</h1>'


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


@app.route('/club_member')
def about_club():
    # get user data
    # 1. get code
    code = request.args.get("code")
    if not code:
        return "缺失code参数"
    
    # 2. get access token
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code".format(APPID, APPSECRET, code)
    with urllib.request.urlopen(url) as response:
        urlResp = json.loads(response.read())

    if "errcode" in urlResp:
        return "获取access_token失败"

    access_token = urlResp['access_token']
    open_id = urlResp['openid']

    # 3 get user data
    url =  'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(access_token, open_id)
    with urllib.request.urlopen(url) as response:
        urlResp = json.loads(response.read())

    if "errcode" in urlResp:
        return "获取用户数据失败"
    else:
        # fill the webpage with user data
        return render_template("club_member.html", user=urlResp)


@app.route('/redirect_member')
def redirect_member():
    redirect_uri = urllib.parse.quote("http://www.scyfc.club/club_member")
    print(redirect_uri)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_userinfo&state=OLIGEI#wechat_redirect".format(APPID, redirect_uri)

    return redirect(url)


@app.route('/pay/one_exercise_per_week')
def pay_one_exerciese_per_week():
    print("get pay request")
    return render_template("pay.html", msg="Diankun")


@app.route('/pay/two_exercises_per_week')
def pay_two_exercieses_per_week():
    print("get pay request")
    return "<h1>pay_two_exercieses_per_week</h1>"

