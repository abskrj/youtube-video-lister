from app import app, collection, cache, client
from flask import render_template, request, redirect, url_for, jsonify
import os
import random
import pymongo

@app.route("/")
def index():
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
@cache.cached(timeout=60, query_string=True)
def dashboard():
    invertList = request.args.get('invertList', -1)
    maxResults = request.args.get('maxResults', 10)
    sortBy = request.args.get('sortBy', 'publishedAt')
    start = request.args.get('start', 0)
    data = collection.find().skip(int(start)).sort([(sortBy, int(invertList))]).limit(int(maxResults))

    return render_template("index.html", data=data)

@app.route("/reqbin-verify.txt")
def reqbin():
    return "", 200

@app.route("/status")
def status():
    application = True
    setup = False
    MongoURI = os.environ.get('MONGODB_URI', None)
    TotalAPISet = int(os.environ.get('TotalAPISet', 1))
    i = str(random.randint(1, TotalAPISet))
    ytAPIKey = os.environ.get(f'YTAPIKey{i}', None)

    if MongoURI is not None and ytAPIKey is not None and ytAPIKey is not None:
        setup = True
    try:
        client = pymongo.MongoClient(MongoURI)
        database = True if client.server_info() is not None else False
    except:
        database = False

    return jsonify(
        status=True,
        database=database,
        application=application,
        setup=setup
    )

@app.route("database-info")
def database_info():
    try:
        client.server_info()
    except Exception as e:
        return str(e), 200
    return "Database up and running", 200
