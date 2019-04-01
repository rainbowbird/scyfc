# -*- coding: utf-8 -*-
# filename: temporay_media.py

import json
import requests
import time
import xmlrpc.client


class TemporaryMedia():
    def __init__(self):
        pass

    def upload_image(self, image_data):
        access_token = self._get_access_token()
        url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token={ACCESS_TOKEN}&type={TYPE}".format(ACCESS_TOKEN=access_token, TYPE="image")
        file_name = str(time.time()).split(".")[0] + 'tmp.jpeg'
        files = {
            'media' : (file_name, image_data, 'image/jpeg')
        }
        result = requests.post(url, files=files)
        r = json.loads(result.text)
        media_id = r.get('media_id')
        return media_id

    def upload_thumb(self):
        pass

    def upload_video(self):
        pass

    def upload_voice(self):
        pass

    def _get_access_token(self):
        proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
        print(proxy.get_access_token())
        return proxy.get_access_token()

    def get_temporary_material(self):
        pass


if __name__ == '__main__':
    myTemporaryMedia = TemporaryMedia()
