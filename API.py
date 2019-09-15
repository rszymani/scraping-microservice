# -*- coding: utf-8 -*-
from celery import Celery
from flask import Flask, request, jsonify, abort, send_file, Response, json
from flask_restful import Api

from Statuses import Statuses
from Service import Service
from Storage import Storage


app = Flask(__name__)
api = Api(app)
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

service = Service()
storage = Storage()
statuses = Statuses()


@celery.task(bind=True)
def scrape_text_task(self, url):
    html = service.get_html_text(url)
    clear_text = service.extract_text_from_html(html)
    storage.save_txt_file(clear_text, self.request.id)


@celery.task(bind=True)
def scrape_images_task(self, url):
    html = service.get_html_text(url)
    img_urls = service.get_images_urls(html)
    images = service.download_images_content(url,  img_urls)
    storage.save_images(images, self.request.id)
    self.update_state(state="WORKING")


@app.route("/scrapeText", methods=["POST"])
def scrape_text():
    url = request.json["url"]
    task = scrape_text_task.delay(url)
    return statuses.status_202(request.url_root, task.id)


@app.route("/scrapeImages", methods=["POST"])
def scrape_images():
    url = request.json["url"]
    task = scrape_images_task.delay(url)
    return statuses.status_202(request.url_root, task.id)


@app.route("/status/<scrape_task_id>")
def get_status(scrape_task_id):
    task = scrape_text_task.AsyncResult(scrape_task_id)
    return jsonify({"task_id": task.id, "status": task.status})


@app.route("/images-id/<images_id>/image/<image>")
def get_image(images_id, image):
    im_path = storage.get_image_path(images_id, image)
    if not im_path:
        abort(404)
    return send_file(im_path)


@app.route("/images/<images_id>")
def get_images_from_id(images_id):
    img_names = storage.list_all_images_dir(images_id)
    if not img_names:
        abort(404)
    img_urls = ["{}images-id/{}/image/{}".format(request.url_root, images_id, name) for name in img_names]
    resp = statuses.images_url_response(images_id, img_urls)
    return resp


@app.route("/textIds")
def get_text_ids():
    text_ids = storage.list_all_text_ids()
    resp = statuses.ids_response(text_ids)
    return resp


@app.route("/imagesIds")
def get_images_ids():
    image_ids = storage.list_all_images_ids()
    resp = statuses.ids_response(image_ids)
    return resp


@app.route("/text/<text_id>")
def get_text(text_id):
    text_file = storage.read_text_from_disk(text_id)
    if not text_file:
        abort(404)
    resp = statuses.text_json_response(text_id, text_file)
    return resp


@app.errorhandler(404)
def not_found(error):
    error_resp = Response(json.dumps({'status': '404', 'message': str(error)}), 404)
    error_resp.headers['Content-type'] = 'application/json'
    return error_resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
