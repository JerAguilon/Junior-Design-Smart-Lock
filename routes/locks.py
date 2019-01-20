from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.user_locks import UserLocks
from managers import lock_manager, user_lock_manager
from parsers.parser_utils import webargs_to_doc
from parsers.request_parsers import POST_USER_LOCK_ARGS, PUT_LOCK_STATUS_ARGS
from parsers.response_parsers import UserLockResponse, UserLockStatusResponse
from security import security_utils
from utils.decorators import authorize


class UserLock(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Returns a list of locks owned by a user',
        parameters=[],
        responseClass=UserLockResponse.name,
        responseMessages=[UserLockResponse.description],
    )
    def get(self, uid, user):
        return user_lock_manager.get_user_locks(uid), 200

    @swagger.operation(
        notes='Adds a valid lock id to a user\'s account',
        parameters=webargs_to_doc(POST_USER_LOCK_ARGS),
        responseClass=UserLockResponse.name,
        responseMessages=[UserLockResponse.description],
    )
    @use_kwargs(POST_USER_LOCK_ARGS, locations=("json", "form"))
    @marshal_with(UserLockResponse.resource_fields)
    def post(self, uid, user, **args):
        user_locks = UserLocks.build(args)
        result = user_lock_manager.create_or_update_user_lock(
            uid, user_locks, should_overwrite=False)
        return result, UserLockResponse.code


class LockStatus(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Updates a lock status',
        parameters=webargs_to_doc(PUT_LOCK_STATUS_ARGS),
        responseClass=UserLockStatusResponse.name,
        responseMessages=[UserLockStatusResponse.description],
    )
    @use_kwargs(PUT_LOCK_STATUS_ARGS, locations=("json", "form"))
    @marshal_with(UserLockStatusResponse.resource_fields)
    def put(self, uid, user, **args):
        lock_id = args['lock_id']
        security_utils.verify_lock_ownership(uid, lock_id)
        return lock_manager.change_lock_status(lock_id, args.get('status'))

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
        ],
        responseClass=UserLockStatusResponse.name,
        responseMessages=[UserLockStatusResponse.description],
    )
    @marshal_with(UserLockStatusResponse.resource_fields)
    def get(self, uid, user, lock_id):
        security_utils.verify_lock_ownership(uid, lock_id)
        return lock_manager.get_lock_status(lock_id)
