from flask import Flask, jsonify
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_cors import CORS

from routes import admin, history, lock_security, locks, users, hardware

from utils.exceptions import AppException


app = Flask(__name__, static_url_path='')
cors = CORS(app)
api = swagger.docs(Api(app), apiVersion="0.1")

api.add_resource(
    admin.Locks,
    "/api/v1/admin/locks"
)
api.add_resource(
    hardware.HardwareLockStatus,
    "/api/v1/hardware/status"
)
api.add_resource(
    history.LockHistory,
    "/api/v1/locks/<lockId>/history"
)
api.add_resource(
    lock_security.LockPassword,
    "/api/v1/locks/<lockId>/passwords/<passwordId>"
)
api.add_resource(
    lock_security.LockPasswords,
    "/api/v1/locks/<lockId>/passwords"
)
api.add_resource(
    lock_security.LockStatus,
    "/api/v1/locks/<lockId>/status"
)
api.add_resource(
    locks.UserLock,
    "/api/v1/locks"
)
api.add_resource(
    users.User,
    "/api/v1/user"
)


@app.errorhandler(AppException)
def exception_handler(error):
    response = jsonify(error.to_dict())
    return response, error.status_code

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


@app.route('/docs')
def docs():
    return app.send_static_file('index.html')

@app.route('/')
def root():
    return "Health check: online"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')
