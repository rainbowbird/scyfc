# -*- coding: utf-8 -*-
# filename: menu.py

import requests
import json
import os
import xmlrpc.client

class Menu():
    def __init__(self, filename='./res/menu.json'):
        self._filename = filename

    def create_menu(self):
        """
        create menu
        """
        with open(self._filename, 'r') as f:
            json_data = json.load(f)

        accessToken = self._get_access_token()
        menu_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={access_token}'.format(access_token=accessToken)
        r = requests.post(menu_url,
                          data=json.dumps(json_data,ensure_ascii=False).encode('utf-8'))
        assert r.status_code == 200
        print("create_menu")
        print(r.text)

    def get_menu(self):
        """
        get menu
        """
        print("get_menu")
        accessToken = self._get_access_token()
        menu_url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={access_token}'.format(access_token=accessToken)
        r = requests.get(menu_url)
        assert r.status_code == 200
        #print(r.json())

    def delete_menu(self):
        """
        delete menu
        """
        accessToken = self._get_access_token()
        menu_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={access_token}'.format(access_token=accessToken)
        r = requests.get(menu_url)
        assert r.status_code == 200
        print("delete_menu")
        print(r.json())

    def _get_access_token(self):
        proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
        #print(proxy.get_access_token())
        return proxy.get_access_token()
