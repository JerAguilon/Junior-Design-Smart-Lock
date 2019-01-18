from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from webargs.flaskparser import use_args

from document_templates.user_locks import UserLocks
from managers import lock_manager, user_lock_manager
from parsers.parsers import POST_USER_LOCK_ARGS, PUT_LOCK_STATUS
from security import security_utils
from utils.decorators import authorize, use_request_form

locks_routes = Blueprint('locks_routes', __name__)

class UserLock(Resource):
    method_decorators = [authorize()]

    def get(self, uid, user):
        return jsonify(user_lock_manager.get_user_locks(uid))

    @use_args(POST_USER_LOCK_ARGS, locations=("json", "form"))
    def post(self, uid, user, args):
        user_locks = UserLocks.build(args)
        result = user_lock_manager.create_or_update_user_lock(uid, user_locks, should_overwrite=False)
        return jsonify(result)

class LockStatus(Resource):
    method_decorators = [authorize()]

    @use_args(PUT_LOCK_STATUS, locations=("json", "form"))
    def put(self, uid, user, args):
        lock_id = args['lock_id']
        security_utils.verify_lock_ownership(uid, lock_id)
        return jsonify(lock_manager.change_lock_status(lock_id, args.get('status')))

    def get(self, uid, user, lock_id):
        security_utils.verify_lock_ownership(uid, lock_id)
        return jsonify(lock_manager.get_lock_status(lock_id))

api = Api(locks_routes)
api.add_resource(UserLock, "/api/v1/userLocks")
api.add_resource(LockStatus, "/api/v1/locks/<lock_id>/lockStatus")
