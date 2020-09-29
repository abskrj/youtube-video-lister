from flask import Flask
import pymongo
import os
import sys

SECRET_KEY = os.urandom(32)

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

MongoURI = os.environ.get('MONGODB_URI', None)

if MongoURI is None:
    sys.exit("\n * MongoDB URI not provided.\n")     

client = pymongo.MongoClient(MongoURI)

db = client.fampay
collection = db.ytvid


from app import views

if __name__ == "__main__":
    app.run()