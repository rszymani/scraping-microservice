# -*- coding: utf-8 -*-
from flask import Flask,request,Response,json,send_file,abort

class Statuses:
    def status_201(self,type="Text"):
        resp = Response(json.dumps({'status': '201',"message":"{} succesfully saved".format(type)}), 201)
        resp.headers['Content-type'] = 'application/json'
        return resp
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
