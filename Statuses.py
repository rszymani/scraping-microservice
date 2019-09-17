# -*- coding: utf-8 -*-
from flask import Response, json


class Statuses:
    def text_json_response(self, text_id, text):
        data = {'status': '200', "text": text, "id": text_id}
        resp = Response(json.dumps(data), 200)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp

    def images_url_response(self, images_id, images):
        data = {'status': '200', "images":images, "id": images_id}
        resp = Response(json.dumps(data), 200)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp

    def ids_response(self, ids):
        data = {'status': '200', "ids": ids}
        resp = Response(json.dumps(data), 200)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp

    def status_202(self, url_root, status_id):
        data = {'status': '202', "message": "accepted, status available in {}status/{}".format(url_root, status_id)}
        resp = Response(json.dumps(data), 202)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp
