from flask import jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.user_locks import UserLocks
from managers import lock_manager, user_lock_manager
from parsers.parser_utils import webargs_to_doc
from parsers.request_parsers import POST_USER_LOCK_ARGS, PUT_LOCK_STATUS_ARGS
from security import security_utils
from utils.decorators import authorize

class UserLock(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Returns a list of locks owned by a user',
        parameters=[]
    )
    def get(self, uid, user):
        return jsonify(user_lock_manager.get_user_locks(uid))

    @swagger.operation(
        notes='Adds a valid lock id to a user\'s account',
        parameters=webargs_to_doc(POST_USER_LOCK_ARGS)
    )
    @use_kwargs(POST_USER_LOCK_ARGS, locations=("json", "form"))
    def post(self, uid, user, **args):
        user_locks = UserLocks.build(args)
        result = user_lock_manager.create_or_update_user_lock(uid, user_locks, should_overwrite=False)
        return jsonify(result)

class LockStatus(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Updates a lock status',
        parameters=webargs_to_doc(PUT_LOCK_STATUS)
    )
    @use_kwargs(PUT_LOCK_STATUS, locations=("json", "form"))
    def put(self, uid, user, **args):
        lock_id = args['lock_id']
        security_utils.verify_lock_ownership(uid, lock_id)
        return jsonify(lock_manager.change_lock_status(lock_id, args.get('status')))

    @swagger.operation(
        notes='Gets the lock status of a user owned lock',
        parameters=[
            {
                'name': 'lock_id',
                'dataType': 'string',
                'description': 'A lock id that the user owns',
                'required': True,
                'paramType': 'path',
            },
        ]
    )
    def get(self, uid, user, lock_id):
        security_utils.verify_lock_ownership(uid, lock_id)
        return jsonify(lock_manager.get_lock_status(lock_id))

