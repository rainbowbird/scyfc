
import hashlib
import random
import string
import time
import xmlrpc.client

import requests


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print(string)
        self.ret['signature'] = hashlib.sha1(string.encode('utf-8')).hexdigest()
        return self.ret


def _get_jsapi_ticket():
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    access_token = proxy.get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(access_token)
    r = requests.get(url = url)
    data = r.json()
    return data['ticket']


def get_jsapi_config(appid, url):
    jsapi_ticket = _get_jsapi_ticket()
    print('jsapi_ticket is {}'.format(jsapi_ticket))

    sig = Sign(jsapi_ticket, url)

    return sig.sign() 
