from flask import Flask, jsonify

from routes import users, locks
from utils.exceptions import AppException

app = Flask(__name__)
app.register_blueprint(users.users_routes)
app.register_blueprint(locks.locks_routes)

@app.errorhandler(AppException)
def handle_error(error):
    print("ERROR")
    print(error)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return "<h1>Health check: SUCCESS</h1>"

