from flask import Flask
import pymongo
import os
import sys
from requests import get
import asyncio
from json import loads

SECRET_KEY = os.urandom(32)

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

MongoURI = os.environ.get('MONGODB_URI', None)

ytAPIKey = os.environ.get('YTAPIKey', None)

if MongoURI is None:
    sys.exit("\n * MongoDB URI not provided.\n")     

client = pymongo.MongoClient(MongoURI)

db = client.fampay
collection = db.ytvid


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
                "thumbnailUrl": data["snippet"]["thumbnails"]["default"]["url"],
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
        query = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&q=football&key={ytAPIKey}"
        try:
            res = get(query)
        except Exception as e:
            print(e)
        res = res.content.decode("utf-8")
        
        print('Received data from YT')

        incoming_data = loads(res)
        data_insert_to_db(incoming_data["items"])
        await asyncio.sleep(10)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_data_from_youtube())

from app import views

if __name__ == "__main__":
    app.run()