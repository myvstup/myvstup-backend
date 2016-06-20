from flask.ext.api import FlaskAPI
from flask_cors import CORS
from pymongo import MongoClient
import os

app = FlaskAPI(__name__)
CORS(app)

db = MongoClient(os.environ.get('MONGODB_URI')).heroku_rcbs36lq

from app import views, models