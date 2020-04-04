# -*- coding: utf-8 -*-
# filename: access_token_server.py 

import json
import threading
import time
import urllib.request
from xmlrpc.server import SimpleXMLRPCServer

_accessToken = ""
_leftTime = 0


class AccessTokenServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._rpc_methods = ['get_access_token', 'update_access_token']
        self._serv = SimpleXMLRPCServer(('127.0.0.1', 9000), logRequests=True, allow_none=True)
        for name in self._rpc_methods:
            self._serv.register_function(getattr(self, name))

    def get_access_token(self):
        # should use a lock to protect the data access
        return _accessToken;

    def update_access_token(self):
        pass

    def run(self):
        self._serv.serve_forever()


def _real_get_access_token():
    global _accessToken
    global _leftTime

    appId = "wxb0bb415e8ca0d547"
    appSecret = "6c40dd3dc217138b77189ce08c748d1c"
    postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))

    with urllib.request.urlopen(postUrl) as response:
        urlResp = json.loads(response.read())
        print(urlResp)

    _accessToken = urlResp['access_token']
    _leftTime = urlResp['expires_in']


if __name__ == '__main__':
    server = AccessTokenServerThread()
    server.start()

    while True:
        if _leftTime > 10:
            time.sleep(2)
            _leftTime -= 2
        else:
            _real_get_access_token()
