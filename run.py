from flask import Flask, jsonify, render_template
from flask_restful import Api
from flask_restful_swagger import swagger

from routes import admin, lock_security, locks, users

from utils.exceptions import AppException

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion="0.1")

api.add_resource(admin.Locks, "/api/v1/admin/locks")
api.add_resource(lock_security.LockPassword, "/api/v1/locks/<lock_id>/passwords/<password_id>")
api.add_resource(lock_security.LockPasswords, "/api/v1/locks/<lock_id>/passwords")
api.add_resource(lock_security.LockStatus, "/api/v1/locks/<lock_id>/status")
api.add_resource(locks.UserLock, "/api/v1/locks")
api.add_resource(users.User, "/api/v1/user")


@app.errorhandler(AppException)
def handle_app_exceptions(error):
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
