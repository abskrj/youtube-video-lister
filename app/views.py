from app import app, collection



@app.route("/")
def index():
    return "hello"

