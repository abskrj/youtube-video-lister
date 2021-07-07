# YouTube Video Lister
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/abhishekraj272/badges/)
![GitHub stars](https://img.shields.io/github/stars/abhishekraj272/youtube-video-lister?style=social)
![GitHub forks](https://img.shields.io/github/forks/abhishekraj272/youtube-video-lister?style=social)
[![GitHub contributors](https://img.shields.io/github/contributors/abhishekraj272/youtube-video-lister.svg)](https://GitHub.com/abhishekraj272/youtube-video-lister/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/abhishekraj272/youtube-video-lister.svg)](https://GitHub.com/abhishekraj272/youtube-video-lister/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/abhishekraj272/youtube-video-lister.svg)](https://GitHub.com/abhishekraj272/youtube-video-lister/pull/)


A python app that searches a predefined query on YouTube using YT Data API and saves it in MongoDB and lists it on the dashboard.

It searches asynchronously in backgroud using Python asyncio and threading library.

Predefined search query: "game"

Time Interval for searching: 60sec

## Table of Contents

-   [Starting Server Locally](#startingserverlocally)
-   [Deploying on Heroku](#deployingonheroku)
-   [Features](#features)
-   [Queries Available](#queriesavailable)
-   [Tools Used](#toolsused)
-   [Development](#development)


## Starting Server Locally
```bash
git clone https://github.com/abhishekraj272/youtube-video-lister.git

cd youtube-video-lister

pip3 install -r requirements.txt

# Set Env Var: MONGODB_URI, TotalAPISet, YTAPIKey1, YTAPIKey2, YTAPIKey3....
# TotalAPISet = count(  YTAPIKey1, YTAPIKey2, YTAPIKey3.... ) 

flask run 
# OR
gunicorn run:app
```

## Deploying on Heroku

```bash
heroku login

heroku create

heroku config:set MONGODB_URI=<MONGODB_URI>
heroku config:set TotalAPISet=<TotalAPISet>
heroku config:set YTAPIKey1=<YTAPIKey1>
.
.
.

git push heroku master

heroku open
```

## Features
1. Shuffles through the provided API Key set every time it searches.
2. View function is cached for 60sec for every args provided.
3. Sort & Filter Options are provided.
4. The data fetched from YT are latest.

## Queries Available
 -   ?invertList=
 -   ?maxResults=
 -  ?sortBy=
 -  ?start=

## Tools Used
1) Flask
2) Pymongo
3) Flask Caching
4) HTML, CSS & JS
5) os, random, datetime, requests, asyncio, json libraries


Note: [Mini YT LOL](https://mini-yt-lol.herokuapp.com/dashboard) is running on a Free Tier MongoDB and Heroku server.

**Screenshot**
![Screenshot](https://github.com/UshasriMavuri1999/youtube-video-lister/blob/master/image/screenshot.png)

***Live: [Mini YT LOL](https://mini-yt-lol.herokuapp.com/dashboard) - Hosted on Heroku***

### Development

Want to contribute? Great!

This repository is the starter code for you. Therefore, I would like to accept your pull requests 😎
