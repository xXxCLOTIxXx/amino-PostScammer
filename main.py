from time import sleep as sl
from colored import fore
from os import system as s
from os import mkdir

import os
import json
import time
import requests
from hmac import new
from typing import Union
from hashlib import sha1
from base64 import b64encode
from threading import Thread

from random import choice
from datetime import datetime
import string
import hmac
from os import urandom
from time import time as timestamp

class Generator():
    def __init__(self):
    	PREFIX = bytes.fromhex("42")
    	SIG_KEY = bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93")
    	DEVICE_KEY = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")\


    def deviceId(self):
        try:
            with open("device.json", "r") as stream:
                data = json.load(stream)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            device = self.generate_device_info()
            with open("device.json", "w") as stream:
                json.dump(device, stream, indent=4)
            with open("device.json", "r") as stream:
                data = json.load(stream)
        return data


    def generate_device_info(self):
        identifier = urandom(20)
        key = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
        mac = hmac.new(key, bytes.fromhex("42") + identifier, sha1)
        device = f"42{identifier.hex()}{mac.hexdigest()}".upper()
        return {
            "device_id": device,
            "user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.5.33562)"
        }

    def signature(self, data) -> str:
        try: dt = data.encode("utf-8")
        except Exception: dt = data
        mac = new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), dt, sha1)
        return b64encode(bytes.fromhex("42") + mac.digest()).decode("utf-8")



class headers():
	def __init__(self, data = None, content_type = None, deviceId: str = None, sid: str = None):
		self.device = Generator().deviceId()
		self.User_Agent = self.device["user_agent"]
		self.sid = sid
		if deviceId!=None:self.device_id = deviceId
		else:self.device_id = self.device["device_id"]


		self.headers = {
			"NDCDEVICEID": self.device_id,
			"Accept-Language": "en-US",
			"Content-Type": "application/json; charset=utf-8",
			"User-Agent": self.User_Agent,
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Upgrade"
		}

		if data is not None:
			self.headers["Content-Length"] = str(len(data))
			self.headers["NDC-MSG-SIG"] = Generator().signature(data=data)
		if self.sid is not None:
			self.headers["NDCAUTH"] = f"sid={self.sid}"
		if content_type is not None:
			self.headers["Content-Type"] = content_type



class LIB:
    def __init__(self, proxies: dict = None, deviceId: str = None):
        self.api = "https://service.narvii.com/api/v1"
        self.proxies = proxies
        self.uid = None
        self.sid = None
        self.session = requests.Session()
        self.web_api = "https://aminoapps.com/api"
        if deviceId:self.deviceId=deviceId
        else:self.deviceId=Generator().deviceId()['device_id']

    def parser(self, data = None, content_type: str = None):
        return headers(data=data, content_type=content_type, deviceId=self.deviceId, sid=self.sid).headers




    def login(self, email: str, password: str):

        data = json.dumps({
            "email": email,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": self.deviceId,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(timestamp() * 1000)
        })
        with self.session.post(f"{self.api}/g/s/auth/login",  headers=self.parser(data=data), data=data, proxies=self.proxies) as response:
            if response.status_code != 200: raise Exception(json.loads(response.text))
            else:json_response = json.loads(response.text)
        self.sid = json_response["sid"]
        self.uid = json_response["account"]["uid"]
        return self.uid



    def get_from_link(self, link: str):


        response = self.session.get(f"{self.api}/g/s/link-resolution?q={link}", headers=self.parser(), proxies=self.proxies)
        if response.status_code != 200: raise Exception(json.loads(response.text))
        else: return json.loads(response.text)["linkInfoV2"]




    def get_blog_info(self, comId: str, blogId: str = None, wikiId: str = None):
        if blogId:
            response = self.session.get(f"{self.api}/x{comId}/s/blog/{blogId}", headers=self.parser(), proxies=self.proxies)
            if response.status_code != 200: raise Exception(json.loads(response.text))
            else: return json.loads(response.text)

        elif wikiId:
            response = self.session.get(f"{self.api}/x{comId}/s/item/{wikiId}", headers=self.parser(), proxies=self.proxies)
            if response.status_code != 200: raise Exception(json.loads(response.text))
            else: return json.loads(response.text)


class Main:
    def __init__(self):
        self.error_color = fore.RED
        self.regular_color = fore.WHITE
        self.input_color = fore.DEEP_SKY_BLUE_2
        self.client = LIB()
        self.start = f"""
        {self.error_color}


        ┏┓╋┏┓
        ┃┃╋┃┃
        ┃┗━┫┃┏━━┳━━┓┏━━┳━━┳━━┳┓┏┳┓┏┳━━┳━┓
        ┃┏┓┃┃┃┏┓┃┏┓┃┃━━┫┏━┫┏┓┃┗┛┃┗┛┃┃━┫┏┛
        ┃┗┛┃┗┫┗┛┃┗┛┃┣━━┃┗━┫┏┓┃┃┃┃┃┃┃┃━┫┃
        ┗━━┻━┻━━┻━┓┃┗━━┻━━┻┛┗┻┻┻┻┻┻┻━━┻┛
        ╋╋╋╋╋╋╋╋┏━┛┃
        ╋╋╋╋╋╋╋╋┗━━┛

        MADE BY Xsarz (Telegram -> @DXsarz)

        GitHub: https://github.com/xXxCLOTIxXx
        Telegram channel: https://t.me/DxsarzUnion
        YouTube: https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q
        Discord server: https://discord.gg/GtpUnsHHT4


        {self.regular_color}
        """

    def clear(self):
        s("clear || cls")
        print(self.start)

    def auth(self):
        try:
            self.client.login(email=input(f"{self.input_color}\nEmail #~ {self.regular_color}"), password=input(f"{self.input_color}\nPassword #~ {self.regular_color}"))
        except Exception as error:
            print(self.error_color,f'\nError login:\n[ - {error} - ]\n',self.regular_color)
            self.auth()

    def gen_name(self, num: int = 8):
        g = ""
        for x in range(num):
            g = g + choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        return g



    def imgInstaller(self, dir: str, url: str, tp: str = 'png'):
        img = requests.get(url)
        out = open(f"{dir}/{self.gen_name()}.{tp}", "wb")
        out.write(img.content)
        out.close()

    def writer(self, dir_name: str, file_name: str, text: str):
        try:mkdir(dir_name)
        except:
            try:
                dir_name+=self.gen_name()
                mkdir(dir_name)
            except:
                dir_name=self.gen_name()
                file_name=dir_name
                mkdir(dir_name)
        main_file = open(f"{dir_name}/{file_name}.txt", "w+", encoding="utf-8")
        main_file.write(text)
        main_file.close()
        return dir_name

    def get_blog_info(self):
        try:
            link_info = self.client.get_from_link(input(f"{self.input_color}\nPost Link #~ {self.regular_color}"))
            return link_info['extensions']['linkInfo']['ndcId'], link_info['extensions']['linkInfo']['objectId']
        except Exception as error:
            print(self.error_color,f'\nFail:\n[ - {error} - ]\n',self.regular_color)
            self.get_blog_info()

    def get_type(self):
        tp = input(f"{self.input_color}1)Blog\n2)Wiki\nType #~ {self.regular_color}")
        if tp != '1':
            if tp != '2':
                print(self.error_color,f'\n[ - Choose post type ! - ]\n',self.regular_color)
                self.get_type()
        return tp


    def main(self):
        self.auth()
        while True:
            comId, postId = self.get_blog_info()
            t = self.get_type()
            if t == '1':
                try:
                    post_info = self.client.get_blog_info(comId=comId, blogId=postId)['blog']
                    try:bg_media_list = post_info['extensions']['style']['backgroundMediaList']
                    except KeyError:bg_media_list='None'
                    try:media_list = post_info['mediaList']
                    except KeyError:media_list='None'
                    content = post_info['content']
                    title = post_info['title']
                    if media_list == None:media_list='None'
                    lst = list()
                    urls = list()
                    if bg_media_list!='None':
                         for i in bg_media_list:lst.append(i)
                    if media_list!='None':
                        for i in media_list:lst.append(i)
                    if lst:
                        for i in lst:
                            urls.append(i[1])
                except Exception as error:
                    print(self.error_color,f'\nFail:\n[ - {error} - ]\n',self.regular_color)
                    continue


            elif t == '2':
                try:
                    post_info = self.client.get_blog_info(comId=comId,  wikiId=postId)
                    try:media_list = post_info['item']['mediaList']
                    except KeyError:media_list='None'
                    try:bg_media_list = post_info['item']['extensions']['style']['backgroundMediaList']
                    except KeyError:bg_media_list='None'
                    content = post_info['item']['content']
                    title = post_info['item']['label']
                    lst = list()
                    urls = list()

                    if media_list == None:media_list='None'
                    if media_list!='None':
                        for i in media_list:lst.append(i)
                    if bg_media_list!='None':
                        for i in bg_media_list:lst.append(i)
                    if lst:
                        for i in lst:
                            urls.append(i[1])
                except Exception as error:
                    print(self.error_color,f'\nFail:\n[ - {error} - ]\n',self.regular_color)
                    continue


            if urls:urls_txt = '\n'.join(urls)
            else:urls_txt='None'
            dir_name=self.writer(dir_name='POST_FOLDER', file_name='main_file', text=f"TITLE:   {title}\nCONTENT:\n\n{content}\n\n\nURL'S:\n{urls_txt}")
            if urls:
                for i in urls:
                    self.imgInstaller(dir=dir_name, url=i)

            print(fore.GREEN,f"\nSuccessfully ! All files are saved in a folder '{dir_name}'{self.regular_color}\n\n")



if __name__ == '__main__':
    main = Main()
    main.clear()
    main.main()
