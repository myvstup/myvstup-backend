# -*- coding: UTF-8 -*-
from app import app
from app import models

from flask import Flask, jsonify, abort, make_response, request

@app.route('/api/v0/points', methods=['POST'])
def add_request():
    print (request.json)
    if type(request.json)!=dict:
        abort(400)
    answer = models.Session.add_points(request.json)

    return jsonify({'userId': str(answer)}),201


#@app.route('/api/v0/get_proba', methods=['GET'])
#def proba_spec():

#    if type(request.json)!=dict:
#        abort(400)

#    response = models.RelevantSpecialization(request.json)

#    return jsonify(response)

#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error': 'Not found'}), 404)
