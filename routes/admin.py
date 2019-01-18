from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from webargs.flaskparser import use_args

from utils.decorators import authorize
from document_templates.lock import Lock
from managers import lock_manager
from parsers.parsers import POST_LOCKS_ARGS

admin_routes = Blueprint('admin_routes', __name__)

class Locks(Resource):
    method_decorators = [authorize(admin=True)]

    @use_args(POST_LOCKS_ARGS, locations=("json", "form"))
    def post(self, uid, user, args):
        lock = Lock.build(args)
        result = lock_manager.add_lock(lock)
        return jsonify(result)

api = Api(admin_routes)
api.add_resource(Locks, "/api/v1/admin/locks")
