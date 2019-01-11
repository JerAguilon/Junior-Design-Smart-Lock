from flask import Flask

from secrets import firebase

app = Flask(__name__)
auth = firebase.auth()

@app.route('/')
def index():
    return "<h1>Sup</h1>"
