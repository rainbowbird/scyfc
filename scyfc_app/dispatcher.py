#!/usr/bin/env python
# -*- coding:utf8 -*-

import importlib
import json
import sys
import time
import xml.etree.ElementTree as ET

from .generate_qrcode import *
from .temporary_media import *

importlib.reload(sys)

class MsgParser(object):
    """
    用于解析从微信公众平台传递过来的参数，并进行解析
    """
    def __init__(self, data):
        self.data = data

    def parse(self):
        self.et = ET.fromstring(self.data)

        self.user = self.et.find("FromUserName").text
        self.master = self.et.find("ToUserName").text
        self.msgtype = self.et.find("MsgType").text

        #self.content = self.et.find("Content").text if self.et.find("Content") is not None else ""
        #self.recognition = self.et.find("Recognition").text if self.et.find("Recognition") is not None else ""
        #self.format = self.et.find("Format").text if self.et.find("Format") is not None else ""
        #self.msgid = self.et.find("MsgId").text if self.et.find("MsgId") is not None else ""
        #self.picurl = self.et.find("PicUrl").text if self.et.find("PicUrl") is not None else ""
        #self.mediaid = self.et.find("MediaId").text if self.et.find("MediaId") is not None else ""
        self.event = self.et.find("Event").text if self.et.find("Event") is not None else ""
        self.eventkey = self.et.find("EventKey").text if self.et.find("EventKey") is not None else ""
        self.ticket = self.et.find("Ticket").text if self.et.find("Ticket") is not None else ""
        self.latitude = self.et.find("Latitude").text if self.et.find("Latitude") is not None else ""
        self.longtitude = self.et.find("Longtitude").text if self.et.find("Longtitude") is not None else ""
        self.precision = self.et.find("Precision").text if self.et.find("Precision") is not None else ""

        return self


class MsgDispatcher(object):
    """
    根据消息的类型，获取不同的处理返回值
    """
    def __init__(self, data):
        parser = MsgParser(data).parse()
        self.msg = parser
        self.handler = MsgHandler(parser)

    def dispatch(self):
        self.result = ""  # 统一的公众号出口数据

        if self.msg.msgtype == "event":
            self.result = self.handler.eventHandle()

        #if self.msg.msgtype == "text":
        #    self.result = self.handler.textHandle()
        #elif self.msg.msgtype == "voice":
        #    self.result = self.handler.voiceHandle()
        #elif self.msg.msgtype == 'image':
        #    self.result = self.handler.imageHandle()
        #elif self.msg.msgtype == 'video':
        #    self.result = self.handler.videoHandle()
        #elif self.msg.msgtype == 'shortvideo':
        #    self.result = self.handler.shortVideoHandle()
        #elif self.msg.msgtype == 'location':
        #    self.result = self.handler.locationHandle()
        #elif self.msg.msgtype == 'link':
        #    self.result = self.handler.linkHandle()

        return self.result


class MsgHandler(object):
    """
    针对type不同，转交给不同的处理函数。直接处理即可
    """
    def __init__(self, msg):
        self.msg = msg
        self.time = int(time.time())

    def eventHandle(self):
        if self.msg.event == "CLICK":
            if self.msg.eventkey == "contact_info":
                print("contact info")
                template = """
                <xml>
                    <ToUserName><![CDATA[{}]]></ToUserName>
                    <FromUserName><![CDATA[{}]]></FromUserName>
                    <CreateTime>{}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{}]]></Content>
                </xml>
                """
                response = template.format(self.msg.user, self.msg.master,
                                           self.time, "手机 1361-192-2613")
                return response

            if self.msg.eventkey == "reservation_qrcode":
                print("get reservation_qrcode request")
                template = """
                <xml>
                    <ToUserName><![CDATA[{}]]></ToUserName>
                    <FromUserName><![CDATA[{}]]></FromUserName>
                    <CreateTime>{}</CreateTime>
                    <MsgType><![CDATA[image]]></MsgType>
                    <Image>
                      <MediaId><![CDATA[{}]]></MediaId>
                    </Image>
                </xml>
                """

                image_data = create_scene_qrcode_image()
                # get media_id
                myTemporaryMedia = TemporaryMedia()
                media_id = myTemporaryMedia.upload_image(image_data)
                response = template.format(self.msg.user, self.msg.master,
                                           self.time, media_id)
                return response
        elif self.msg.event == "VIEW":
            print("get view event request: eventkey {}".format(self.msg.eventkey))

            template = """
            <xml>
                <ToUserName><![CDATA[{}]]></ToUserName>
                <FromUserName><![CDATA[{}]]></FromUserName>
                <CreateTime>{}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{}]]></Content>
            </xml>
            """
            response = template.format(self.msg.user, self.msg.master,
                                        self.time, self.msg.eventkey)
            return response


    def textHandle(self, user='', master='', time='', content=''):
        template = """
        <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>{}</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[{}]]></Content>
         </xml>
        """
        # 对用户发过来的数据进行解析，并执行不同的路径
        try:
            response = get_response_by_keyword(self.msg.content)
            if response['type'] == "image":
                result = self.imageHandle(self.msg.user, self.msg.master, self.time, response['content'])
            elif response['type'] == "music":
                data = response['content']
                result = self.musicHandle(data['title'], data['description'], data['url'], data['hqurl'])
            elif response['type'] == "news":
                items = response['content']
                result = self.newsHandle(items)
            # 这里还可以添加更多的拓展内容
            else:
                response = get_turing_response(self.msg.content)
                result = template.format(self.msg.user, self.msg.master, self.time, response)
            #with open("./debug.log", 'a') as f:
            #   f.write(response['content'] + '~~' + result)
            #    f.close()
        except Exception as e:
            with open("./debug.log", 'a') as f:
               f.write("text handler:"+str(e.message))
               f.close()
        return result

    def imageHandle(self, user='', master='', time='', mediaid=''):
        template = """
        <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>{}</CreateTime>
             <MsgType><![CDATA[image]]></MsgType>
             <Image>
             <MediaId><![CDATA[{}]]></MediaId>
             </Image>
         </xml>
        """
        if mediaid == '':
            response = self.msg.mediaid
        else:
            response = mediaid
        result = template.format(self.msg.user, self.msg.master, self.time, response)
        return result

    def voiceHandle(self):
        response = get_turing_response(self.msg.recognition)
        result = self.textHandle(self.msg.user, self.msg.master, self.time, response)
        return result

    def musicHandle(self, title='', description='', url='', hqurl=''):
        template = """
        <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>{}</CreateTime>
             <MsgType><![CDATA[music]]></MsgType>
             <Music>
             <Title><![CDATA[{}]]></Title>
             <Description><![CDATA[{}]]></Description>
             <MusicUrl><![CDATA[{}]]></MusicUrl>
             <HQMusicUrl><![CDATA[{}]]></HQMusicUrl>
             </Music>
             <FuncFlag>0</FuncFlag>
        </xml>
        """
        response = template.format(self.msg.user, self.msg.master, self.time, title, description, url, hqurl)
        return response

    def videoHandle(self):
        return 'video'

    def shortVideoHandle(self):
        return 'shortvideo'

    def locationHandle(self):
        return 'location'

    def linkHandle(self):
        return 'link'
