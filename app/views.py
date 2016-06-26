# -*- coding: UTF-8 -*-
from app import app
from app import models

from flask import abort, request
import json

@app.route('/api/v0/points', methods=['POST','GET'])
def add_request():

    if request.method == 'GET':
        return {'status':'get_ok'}

    if request.method == 'POST':
        data = {'userId': str(models.Tools.add_points(request.data))	}
        return data, 201

@app.route('/api/v0/get_proba', methods=['POST'])
def proba_spec():

    response = models.RelevantSpecialization(request.data).count_proba()

    return response, 200

@app.errorhandler(404)
def not_found(error):
    return {'Attention':'The world is mine!'}