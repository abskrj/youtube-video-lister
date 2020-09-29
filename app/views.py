from app import app, collection
from flask import render_template, request, redirect, url_for
from flask_wtf.csrf import CsrfProtect
import re
from json import loads
import dateutil

@app.route("/")
def index():
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
# @cache.cached(timeout=60, query_string=True)
def dashboard():
    invertList = request.args.get('invertList', -1)
    maxResults = request.args.get('maxResults', 10)
    sortBy = request.args.get('sortBy', 'publishedAt')

    data = collection.find().sort([(sortBy, int(invertList))]).limit(int(maxResults))
    
    return render_template("index.html", data=data)