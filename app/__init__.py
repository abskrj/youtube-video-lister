from flask import Flask
import pymongo
import os
import sys
from requests import get
import asyncio
from json import loads
import threading
from flask_caching import Cache
import datetime

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "filesystem", 'CACHE_DIR': 'cache-directory', 'CACHE_THRESHOLD': 500})

app.config['SECRET_KEY'] = SECRET_KEY

MongoURI = os.environ.get('MONGODB_URI', "mongodb+srv://abhishek:Asdfg#1hjkl@cluster0.nkell.mongodb.net/fampay?retryWrites=true&w=majority")

ytAPIKey = os.environ.get('YTAPIKey', "AIzaSyBlR2Av2WHgV6yDlLLllJXBUL2GdyyCuOE")

if MongoURI is None:
    sys.exit("\n * MongoDB URI not provided.\n")     

client = pymongo.MongoClient(MongoURI)

# Selecting database
db = client.fampay

# Selecting collection
collection = db.ytvid

# Custom templat filter to convert time format
@app.template_filter()
def fmdatetime(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")

# Function to insert data into db
def data_insert_to_db(incoming_data):
    """
    Function to insert video data to database.
    """

    print('inserting data')

    try:
        for data in incoming_data:
            # Key to find if data is present or not.
            key = {'videoId': data["id"]["videoId"]}

            to_be_inserted = {
                "videoId": data["id"]["videoId"],
                "videoTitle": data["snippet"]["title"],
                "description": data["snippet"]["description"],
                "publishedAt": data["snippet"]["publishedAt"],
                "thumbnailUrl": data["snippet"]["thumbnails"]["medium"]["url"],
                "channelName": data["snippet"]["channelTitle"]
            }

            # Checks videoId already present or not.
            collection.update(key, to_be_inserted, upsert=True)
    except Exception as e:
        print(e)


async def get_data_from_youtube():
    """
    Function to get data from Youtube useing API.
    """
    while True:
        query = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&q=gdp&key=AIzaSyBlR2Av2WHgV6yDlLLllJXBUL2GdyyCuOE"
        try:
            res = get(query)
        except Exception as e:
            print(e)
        
        if res.status_code != 200:
            print(res.content)
            if res.status_code == 403:
                query = 

        res = res.content.decode("utf-8")
        
        print('Received data from YT')

        incoming_data = loads(res)
        data_insert_to_db(incoming_data["items"])
        await asyncio.sleep(60)

# def loop_in_thread(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(get_data_from_youtube())

# loop = asyncio.get_event_loop()
# t = threading.Thread(target=loop_in_thread, args=(loop,))
# t.start()

from app import views

if __name__ == "__main__":
    app.run()