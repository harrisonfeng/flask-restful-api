#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''Code snippet for flask api example

This code snippet is created based on 
http://blog.luisrei.com/articles/flaskrest.html
I made slightly modification on the original examples.

The modification is only for learning flask purpose.

'''
#
#

import json

from flask import Flask
from flask import url_for
from flask import jsonify
from flask import request
from flask import Response
from functools import wraps

app = Flask(__name__)


# ----------------------------------------------------------------------------
# Resources
# ----------------------------------------------------------------------------
@app.route('/v1/')
def root():
    return jsonify({'data': 'welcome api v1'})


@app.route('/v1/articles')
def articles():
    return jsonify({'data': 'List of' + url_for('articles')})


@app.route('/v1/articles/<int:articleid>')
def article(articleid):
    return jsonify({'data': 'You are reading ' + str(articleid)})

@app.route('/v1/data')
def hello():
    if 'name' in request.args:
        return jsonify({'data': 'Hello, %s' % request.args['name']})
    else:
        return jsonify({'data': 'Hello, user'})


# ----------------------------------------------------------------------------
# Request methods (Http verbs)
# ----------------------------------------------------------------------------
@app.route('/methods', methods=['GET', 'POST', 'PATCH',
                                'PUT', 'DELETE'])
def echo():
    if request.method == 'GET':
        return jsonify({'method': 'GET'})
    if request.method == 'POST':
        return jsonify({'method': 'POST'})
    if request.method == 'PUT':
        return jsonify({'method': 'PUT'}) 
    if request.method == 'DELETE':
        return jsonify({'method': 'DELETE'}) 
    if request.method == 'PATCH':
        return jsonify({'method': 'PATCH'}) 


# ----------------------------------------------------------------------------
# Request data & headers
# Accessing the HTTP headers is done using the request.headers dictionary( "
# dictionary-like object") and the request data using request.data string.
# if the mimetype is application.json, request.json will contain the parsed
# json.
# ----------------------------------------------------------------------------
@app.route('/messages', methods=['POST'])
def message():
    if request.headers['Content-Type'] == 'text/plain':
        return "text_msg: {0}".format(request.data)
    elif request.headers['Content-Type'] == 'application/json':
        return jsonify({'text_msg': request.data})
    elif request.headers['Content-Type'] == 'application/octet-stream':
        with open('/tmp/api_bin', 'wb') as f:
            f.write(request.data)
        return jsonify({'msg': 'successful'}) 
    else:
        return Response(json.dumps({'msg': 'unsupported media type'}), 
                                status=415, mimetype='application/json') 


# ----------------------------------------------------------------------------
# Response
# Responses are handled by flask.Response class
# ----------------------------------------------------------------------------
@app.route('/datas', methods=['GET'])
def datas():
    data = {

	'action': 'fucking the world', 
        'number': 10000
        }
#   resp = Response(json.dumps(data, sort_keys=True, indent=4), status=200, 
#                              mimetype='application/json')
    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Link'] = 'http://fucking.com'
    return resp

# ----------------------------------------------------------------------------
# Status codes and Errors
# ----------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error=None):
    msg = {
          
          'status': 404,
          'msg': 'Not found at your requested URL: {0}'.format(request.url)
        }
    resp = jsonify(msg)
    resp.status_code = 404
    return resp


@app.route('/users/<int:user_id>', methods=['GET'])
def users(user_id):
    users = { 
        
        '1': 'john',
        '2': 'bob',
        '3': 'mark',
    }
    user = {}
    if str(user_id) in users:
        user = { 
            'id': user_id,
            'name': users.get(str(user_id), None)
        }
        return jsonify(user)
    else:
        return not_found()

# ------------------------------------------------------------
# authorization
# ------------------------------------------------------------

def check_auth(username, password):
    

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug=True)
