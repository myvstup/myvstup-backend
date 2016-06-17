from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

db = MongoClient(os.environ.get('MONGODB_URI')).heroku_rcbs36lq

from app import views, models