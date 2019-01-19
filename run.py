from flask import Flask, jsonify, render_template
from flask_restful import Api
from flask_restful_swagger import swagger

from routes import admin, locks, users

from utils.exceptions import AppException
from secrets import DB  # do not remove, DB needs to be initialized at app start

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion="0.1")

api.add_resource(admin.Locks, "/api/v1/admin/locks")
api.add_resource(locks.LockStatus, "/api/v1/locks/<lock_id>/lockStatus")
api.add_resource(locks.UserLock, "/api/v1/userLocks")
api.add_resource(users.User, "/api/v1/user")

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

