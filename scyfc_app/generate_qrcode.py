#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from io import StringIO, BytesIO
import json
import qrcode
import requests
import xmlrpc.client

def get_qrcode_url(access_token, scene_id):
    data = {
        "expire_seconds": 1000,
        "action_name": "QR_SCENE",
        "action_info": {
            "scene": {
                "scene_id": scene_id
            }
        }
    }
    data = json.dumps(data)
    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={ACCESS_TOKEN}".format(ACCESS_TOKEN=access_token)
    try:
        data_result = requests.post(url, data=data)
        result = json.loads(data_result.text)
        url = result["url"]
        print("url:" + url)
        return url
    except:
        print("生成专属参数二维码错误")

def get_qrcode_image_data(url):
    buf = BytesIO()

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")
    imgW, imgH = img.size

    w1, h1 = map(lambda x: x//4, img.size)
    icon = Image.open("./res/scyfc_club.jpeg")
    iconW, iconH = icon.size
    w1 = w1 if w1 < iconW else iconW
    h1 = h1 if h1 < iconH else iconH
    icon = icon.resize((w1, h1))

    img.paste(icon, ((imgW-w1)//2, (imgH-h1)//2))
    #icon.paste(img, (50, 50), img)
    img.save(buf, format="png")
    file_content = buf.getvalue()
    return file_content

def create_scene_qrcode_image():
    """
    Create WeChat scene qrcode image
    """
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    access_token = proxy.get_access_token()
    scene_id = 100000000

    url = get_qrcode_url(access_token, scene_id)
    image_data = get_qrcode_image_data(url)

    return image_data

