from flask import Flask
import pymongo
import os, sys
from requests import get
import asyncio
from json import loads
import threading
from flask_caching import Cache
import datetime
import random

# For generating random number based on time, used in shuffling APIs.
random.seed(a=None, version=2)

app = Flask(__name__)

# Cache type, directory and threshold is defined here
cache = Cache(app, config={"CACHE_TYPE": "filesystem", 'CACHE_DIR': 'cache-directory', 'CACHE_THRESHOLD': 50})

# Gets the MongoDB URI from env var
MongoURI = os.environ.get('MONGODB_URI', None)

# Set the total number of API Keys are provided for shuffeling
TotalAPISet = os.environ.get('TotalAPISet', 1)

if MongoURI is None:
    sys.exit("\n * MongoDB URI not provided.\n")


# MongoDB client is initialised
client = pymongo.MongoClient(MongoURI)

# Selecting database
db = client.fampay

# Selecting collection
collection = db.ytvid

# Custom template filter to convert time format
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

# Async function for getting data from YT API
async def get_data_from_youtube():
    """
    Function to get data from Youtube useing API.
    """
    # Generates random number between 1 and total APIs provided 
    i = random.randint(1, TotalAPISet)
    
    # Gets the API Key from env var
    ytAPIKey = os.environ.get(f'YTAPIKey{i}', None)

    if ytAPIKey is None:
        sys.exit("\n * Google API Key not provided.\n")

    # Query for getting data from YouTube
    query = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&q=gdp&key={ytAPIKey}"

    while True:
        try:
            res = get(query)
        except Exception as e:
            print(e)
        
        # Checks if data is fetched or not
        if res.status_code == 200:

            res = res.content.decode("utf-8")
            print('Received data from YT')
            incoming_data = loads(res)
            data_insert_to_db(incoming_data["items"])
        
        else:
            # Please see line 26-30 for details
            i = random.randint(1, TotalAPISet)
            ytAPIKey = os.environ.get(f'YTAPIKey{i}', None)
            query = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&q=gdp&key={ytAPIKey}"

        await asyncio.sleep(60)

# Function for initialising Async Loop
def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_data_from_youtube())

# Puts the get request in background 
loop = asyncio.get_event_loop()
t = threading.Thread(target=loop_in_thread, args=(loop,))
t.start()

# imports views from views.py
from app import views

if __name__ == "__main__":
    app.run()