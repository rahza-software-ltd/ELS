from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from functools import wraps
from flask import Flask, jsonify, request, abort, current_app, session, url_for
from config import config as config
from functions import iohandler
from flask_cors import CORS
from flask_inputs.validators import JsonSchema
from functions import fstack_json_schema
import json
import hashlib
import netifaces
import requests
import socket

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

connection = config.connection()
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
dbconn = connection.startConnection()
handler = iohandler.Ioapi()
api = Api(app)
cursor = dbconn.cursor()

class Test(Resource):
    def post(self):
        return jsonify({'success': "working"})

class logout(Resource):
    def post(self):
        session.pop('email', None)
        session.pop('userid', None)
        return jsonify({'StatusCode' : '200', 'message':'logged Out'})

class Authenticate(Resource):
    def post(self):
        try:
            req_data = request.get_json(force=True)
            expectedFields = ['email','password']
            missing = handler.checkJson(expectedFields,req_data)
            if missing:
                return jsonify({'StatusCode' : '200', 'Missing field': missing})
            __email = req_data['regno']
            __password = req_data['password']

            if __regno in session:
                return jsonify({'StatusCode' : '201', 'message':'sessionActive'})

            cursor.execute("SELECT COUNT(1) FROM users WHERE email = {};".format(__email))
            if not cursor.fetchone()[0]:
                return jsonify({'StatusCode' : '201', 'message':'Invalid email'})

            cursor.execute("SELECT userid,password,disabled,regno FROM users WHERE email = {};".format(__email))

            for row in cursor.fetchall():
                # if hashlib.md5(__password).hexdigest()  == row[1]:
                # print(row[2])
                if row[2] == 0:
                    if __password  == row[1]:
                        session['email'] = __email
                        session['userid'] = row[0]
                        return jsonify({'StatusCode' : '200', 'message':'successfull', 'sessionId':session['userid'], "sessionRegno":session['regno']})
                    else:
                        return jsonify({'StatusCode':'201', 'message':'Invalid password', 'data':count})
                elif row[2] == 2:
                    return jsonify({'StatusCode':'201', 'message':'account blocked for several transfer trial'})
                else:
                    return jsonify({'StatusCode':'201', 'message':'suspisious transaction on account'})
        except Exception as e:
            return {'error': str(e)}
        except TypeError:
            return jsonify({'StatusCode' : '400', 'message':'Invalid json input'})


        