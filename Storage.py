# -*- coding: utf-8 -*-
from flask import Flask,request,Response,json,send_file,abort
from flask_restful import Resource, Api

import uuid
import html2text
import re
import string
import requests

from urllib.parse import urlparse

import os

from bs4 import BeautifulSoup as soup

class Storage:
    def create_images_dir(self,id):
        images_dir = "scraped_resources/images/{}".format(id)
        if not os.path.isdir(images_dir):
            os.mkdir(images_dir)

    def save_txt_file(self,text,id):
        with open('scraped_resources/texts/{}.txt'.format(id), 'w', encoding='utf8') as file:
            file.write(text)
        return True

    def save_images(self,url,img_urls,id):
        self.create_images_dir(id)
        netloc = urlparse(url).netloc
        scheme = urlparse(url).scheme
        site = "{}://{}".format(scheme,netloc)
        for url in img_urls:
            filename = url[url.rfind("/")+1:]
            if any(x in filename for x in ['jpg','png','jpeg','tiff']):
                filename = re.sub("[^(A-Za-z.\-_0-9)]","",filename)
                with open("scraped_resources/images/{}/{}".format(id,filename), 'wb') as f:
                    if 'http' not in url:
                        url = '{}{}'.format(site, url)
                    img_response = requests.get(url)
                    f.write(img_response.content)
        return True


    def read_text_from_disk(self,id):
        file_name = "scraped_resources/texts/{}.txt".format(id)
        if not os.path.isfile(file_name):return None
        with open(file_name, 'r', encoding='utf8') as f:
            file_content = f.read()
        return file_content

    def list_all_images_dir(self,id):
        dir = "scraped_resources/images/{}/".format(id)
        if not os.path.isdir(dir):
            return None
        return os.listdir(dir)

    def list_all_images_ids(self):
        dir = "scraped_resources/images"
        if not os.path.isdir(dir):
            return None
        return os.listdir(dir)
    def list_all_text_ids(self):
        dir = "scraped_resources/texts"
        if not os.path.isdir(dir):
            return None
        ids = [file[:-4] for file in os.listdir(dir)]
        return ids
    def get_image_path(self,id,image):
        image_path = "scraped_resources/images/{}/{}".format(id,image)
        if not os.path.isfile(image_path):
            return None
        return image_path
