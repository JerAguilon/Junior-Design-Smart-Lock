from flask import Flask, jsonify, render_template

from routes import users, locks, admin
from utils.exceptions import AppException
from secrets import DB  # do not remove, DB needs to be initialized at app start

app = Flask(__name__)
app.register_blueprint(users.users_routes)
app.register_blueprint(locks.locks_routes)
app.register_blueprint(admin.admin_routes)

@app.errorhandler(AppException)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# Return validation errors as JSON
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

@app.route('/')
def index():
    return render_template('/index.html')

