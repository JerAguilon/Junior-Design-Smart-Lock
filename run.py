from flask import Flask

import pdb; pdb.set_trace()
from .secrets import DB

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Sup</h1>"
