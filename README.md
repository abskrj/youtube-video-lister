# YouTube Video Lister

A python app which searchs predefined query on YouTube using YT Data API and saves it in MongoDB and lists it on dashboard.

It searches asynchronously in backgroud using Python asyncio and threading library.

Predefined search query: "game"

Time Interval for searching: 60sec

### Live: [Mini YT LOL](https://mini-yt-lol.herokuapp.com/dashboard) - Hosted on Heroku

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
1. ?invertList=
2. ?maxResults=
3. ?sortBy=
4. ?start=

## Tools - Used:
1.Flask
2.Pymongo
3.Flask Caching

Note: [Mini YT LOL](https://mini-yt-lol.herokuapp.com/dashboard) is running on a Free Tier MongoDB and Heroku server.
