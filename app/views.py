from app import app, collection, cache
from flask import render_template, request, redirect, url_for
import re
from json import loads

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