# -*- coding: UTF-8 -*-
from app import app
from app import models
import time
from flask import abort, request
import json

@app.route('/api/v0/get_proba', methods=['POST'])
def proba_spec():

    if request.method == 'POST':

        try: request.data['certificateScore']
        except KeyError:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400

        response = models.RelevantSpecialization(request.data).count_proba()

    return response, 200

@app.route('/api/v0/auto_complete_data', methods=['GET'])
def auto_complete_data():

    if request.method == 'GET':
        response = models.AutoCompleteData().get_file()
        response = models.AutoCompleteData().alpha_sorting(response)

    return response, 200

@app.errorhandler(404)
def not_found(error):
    return {'Attention':'The world is mine!'}