from flask import Flask,request,Response,json,send_file,abort

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

class Service:
    def get_html_text(self,url):
        r = requests.get(url)
        return r.text


    def extract_text_from_html(self,html):
        h = html2text.HTML2Text()
        h.wrap_links = False
        h.skip_internal_links = True
        h.inline_links = True
        h.ignore_anchors = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.ignore_links = True
        output_text = h.handle(html)
        output = re.sub(r'\w*\d\w*', ' ', output_text )
        urls_removed = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', output)
        exclude = set(string.punctuation)
        clear_text = ''.join(ch for ch in urls_removed if ch not in exclude)
        clear_text = re.sub('\s+',' ',clear_text )
        return clear_text.strip()
    def get_images_urls(self,html):
        soup_page = soup(html,features="html.parser")
        img_tags = soup_page.find_all('img')
        img_urls = []
        for img in img_tags:
            url = img.get('src', img.get('data-src'))
            if url:
                img_urls.append(url)
        return img_urls
class Statuses:
    def status_201(self,type="Text"):
        resp = Response(json.dumps({'status': '201',"message":"{} succesfully saved".format(type)}), 201)
        resp.headers['Content-type'] = 'application/json'
        return resp
    def status_404(self):
        error_resp = Response(json.dumps({'status': '404','message': 'Not found'}), 404)
        error_resp.headers['Content-type'] = 'application/json'
        return error_resp
    def text_json_response(self,id,text):
        data = {'status': '200',"text":text,"id":id}
        resp = Response(json.dumps(data), 200)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp
    def images_url_response(self,id,images):
        data = {'status': '200',"images":images,"id":id}
        resp = Response(json.dumps(data), 200)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp
    def ids_response(self,ids):
        data = {'status': '200',"ids":ids}
        resp = Response(json.dumps(data), 200)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp
'-------------------------------------------------------------'
app = Flask(__name__)
service = Service()
storage = Storage()
statuses = Statuses()

@app.route('/scrape_text',methods=["POST"])
def scrape_text():
    url = request.json["url"]
    html = service.get_html_text(url)
    clear_text = service.extract_text_from_html(html)
    uuid_resource = str(uuid.uuid4())
    file_saved = storage.save_txt_file(clear_text,uuid_resource)
    response = statuses.status_201(type="Text") if file_saved else abort(404)
    return response

@app.route('/scrape_images',methods=["POST"])
def scrape_images():
    url = request.json["url"]
    html = service.get_html_text(url)
    img_urls = service.get_images_urls(html)
    uuid_resource = str(uuid.uuid4())
    images_saved = storage.save_images(url,img_urls,uuid_resource)
    response = statuses.status_201(type="Images") if images_saved else abort(404)
    return response

@app.route('/text/<id>')
def get_text(id):
    text_file = storage.read_text_from_disk(id)
    if not text_file: abort(404)
    resp = statuses.text_json_response(id,text_file)
    return resp

@app.route('/images/<id>')
def get_images(id):
    img_names = storage.list_all_images_dir(id)
    if not img_names: abort(404)
    img_urls = ["{}images-id/{}/image/{}".format(request.url_root,id,name) for name in img_names]
    resp = statuses.images_url_response(id,img_urls)
    return resp

@app.route('/list-text-ids')
def list_text_ids():
    text_ids = storage.list_all_text_ids()
    resp = statuses.ids_response(text_ids)
    return resp

@app.route('/list-images-ids')
def list_images_ids():
    image_ids = storage.list_all_images_ids()
    resp = statuses.ids_response(image_ids)
    return resp

@app.route('/images-id/<id>/image/<image>')
def open_image(id,image):
    im_path = storage.get_image_path(id,image)
    if not im_path: abort(404)
    return send_file(im_path)
@app.errorhandler(404)
def not_found(error):
    response = statuses.status_404()
    return response

if __name__ == '__main__':
    app.run(debug=True)
