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
from Statuses import Statuses
from Service import Service
from Storage import Storage

app = Flask(__name__)

api = Api(app)

class ScrapeText(Resource):
    def __init__(self,**kwargs):
        self.service = kwargs['service']
        self.storage = kwargs['storage']
        self.statuses = kwargs['statuses']
    def post(self):
        url = request.json["url"]
        html = self.service.get_html_text(url)
        clear_text = self.service.extract_text_from_html(html)
        uuid_resource = str(uuid.uuid4())
        file_saved = self.storage.save_txt_file(clear_text,uuid_resource)
        response = self.statuses.status_201(type="Text") if file_saved else abort(404)
        return response
class ScrapeImages(Resource):
    def __init__(self,**kwargs):
        self.service = kwargs['service']
        self.storage = kwargs['storage']
        self.statuses = kwargs['statuses']
    def post(self):
        url = request.json["url"]
        html = service.get_html_text(url)
        img_urls = service.get_images_urls(html)
        uuid_resource = str(uuid.uuid4())
        images_saved = storage.save_images(url,img_urls,uuid_resource)
        response = statuses.status_201(type="Images") if images_saved else abort(404)
        return response
class Text(Resource):
    def __init__(self,**kwargs):
        self.service = kwargs['service']
        self.storage = kwargs['storage']
    def get(self,id):
        text_file = storage.read_text_from_disk(id)
        if not text_file: abort(404)
        resp = statuses.text_json_response(id,text_file)
        return resp
class Images(Resource):
    def __init__(self,**kwargs):
        self.service = kwargs['service']
        self.storage = kwargs['storage']
    def get(self,id):
        img_names = storage.list_all_images_dir(id)
        if not img_names: abort(404)
        img_urls = ["{}images-id/{}/image/{}".format(request.url_root,id,name) for name in img_names]
        resp = statuses.images_url_response(id,img_urls)
        return resp
class TextIDs(Resource):
    def __init__(self,**kwargs):
        self.service = kwargs['service']
        self.storage = kwargs['storage']
    def get(self):
        text_ids = storage.list_all_text_ids()
        resp = statuses.ids_response(text_ids)
        return resp
class ImagesIDs(Resource):
    def __init__(self,**kwargs):
        self.service = kwargs['service']
        self.storage = kwargs['storage']
    def get(self):
        image_ids = storage.list_all_images_ids()
        resp = statuses.ids_response(image_ids)
        return resp
class FileSender(Resource):
    def __init__(self,**kwargs):
        self.service = kwargs['service']
        self.storage = kwargs['storage']
    def get(self,id,image):
        im_path = storage.get_image_path(id,image)
        if not im_path: abort(404)
        return send_file(im_path)

@app.errorhandler(404)
def not_found(error):
    error_resp = Response(json.dumps({'status': '404','message': 'Not found'}), 404)
    error_resp.headers['Content-type'] = 'application/json'
    return error_resp

service = Service()
storage = Storage()
statuses = Statuses()
resource_class_kwargs ={ 'service': Service(),'storage':Storage(),'statuses':Statuses() }
api.add_resource(ScrapeText, '/scrape-text',resource_class_kwargs=resource_class_kwargs)
api.add_resource(ScrapeImages, '/scrape-images',resource_class_kwargs=resource_class_kwargs)

api.add_resource(Text, '/text/<id>',resource_class_kwargs=resource_class_kwargs)
api.add_resource(Images, '/images/<id>',resource_class_kwargs=resource_class_kwargs)

api.add_resource(TextIDs, '/list-text-ids',resource_class_kwargs=resource_class_kwargs)
api.add_resource(ImagesIDs, '/list-images-ids',resource_class_kwargs=resource_class_kwargs)
api.add_resource(FileSender, '/images-id/<id>/image/<image>',resource_class_kwargs=resource_class_kwargs)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
