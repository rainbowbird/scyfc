#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import xmlrpc.client

import requests


class PermanentMedia():
    def __init__(self):
        pass

    def get_image(self):
        accessToken = self._get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}'.format(access_token=accessToken)
        request_data = {
            "type": "image",
            "offset": 0,
            "count": "20"
        }
        data = json.dumps(request_data)
        r = requests.post(url, data=data)

        with open('image_material.json', 'w') as f:
            json.dump(r.text, f)

    def get_video(self):
        accessToken = self._get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}'.format(access_token=accessToken)
        request_data = {
            "type": "video",
            "offset": 0,
            "count": "20"
        }
        data = json.dumps(request_data)
        r = requests.post(url, data=data)

        with open('video_material.json', 'w') as f:
            json.dump(r.text, f)

    def get_voice(self):
        accessToken = self._get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}'.format(access_token=accessToken)
        request_data = {
            "type": "voice",
            "offset": 0,
            "count": "20"
        }
        data = json.dumps(request_data)
        r = requests.post(url, data=data)

        with open('voice_material.json', 'w') as f:
            json.dump(r.text, f)

    def get_news(self):
        accessToken = self._get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}'.format(access_token=accessToken)
        request_data = {
            "type": "news",
            "offset": 0,
            "count": "20"
        }
        data = json.dumps(request_data)
        r = requests.post(url, data=data)

        with open('news_material.json', 'w') as f:
            json.dump(r.json(), f, indent=4, ensure_ascii=False, sort_keys=True)

    def _get_access_token(self):
        proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
        print(proxy.get_access_token())
        return proxy.get_access_token()

if __name__ == "__main__":
    myPermanentMedia = PermanentMedia()
    myPermanentMedia.get_news()
