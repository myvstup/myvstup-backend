# -*- coding: UTF-8 -*-
from app import app
from app import models

from flask import Flask, jsonify, abort, Response, request
import json

@app.route('/api/v0/points', methods=['POST','GET'])
def add_request():
    encoding = request.data.decode('utf8')
    if len(encoding)!=0:
        data = {'userId': str(models.Session.add_points(json.loads(encoding)))}
    else :
        data = {"Error":"Wrong data"}

    resp = jsonify(data)
    resp.status = 'OK'
    resp.status_code = 200
    resp.content_type = 'application/json;charset=utf-8'
    resp.headers = {'Content-Type' : 'application/json;charset=utf-8',
                    'Access-Control-Allow-Credentials' : 'true',
                    'Access-Control-Allow-Origin'    : '*'}

    return resp

@app.route('/api/v0/get_proba', methods=['GET'])
def proba_spec():

    try : encoding = request.data.decode('utf8')
    except TypeError : abort (400)

    response = models.RelevantSpecialization.count_proba(json.loads(encoding))

    return jsonify(response)

@app.errorhandler(404)
def not_found(error):

    resp = jsonify({'error': 'Not found'})
    resp.status_code = 404
    resp.headers['Access-Control-Request-Headers'] = '*'

    return resp