from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.history import StateChange
from document_templates.user_locks import UserLocks
from managers import user_lock_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import DeleteUserLockArgs, PostUserLockArgs
from parsers.response_parsers import UserLockResponse
from security import security_utils
from utils.decorators import authorize, record_history


class UserLock(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Returns a list of locks owned by a user',
        parameters=[],
        responseClass=UserLockResponse.__name__,
        responseMessages=[UserLockResponse.description],
        tags=['Locks'],
    )
    def get(self, uid, user):
        return user_lock_manager.get_user_locks(uid), UserLockResponse.code

    @swagger.operation(
        notes='Adds a valid lock id to a user\'s account',
        parameters=[PostUserLockArgs.schema],
        responseClass=UserLockResponse.__name__,
        responseMessages=[UserLockResponse.description],
        tags=['Locks'],
    )
    @use_kwargs(PostUserLockArgs.resource_fields, locations=("json", "form"))
    @marshal_with_parser(UserLockResponse)
    @record_history(state_changes={
        UserLockResponse.code: StateChange.USER_LOCK_DELETED
    })
    def post(self, uid, user, **args):
        user_locks = UserLocks.build(args)
        result = user_lock_manager.create_or_update_user_lock(
            uid, user_locks, should_overwrite=False)
        return result, UserLockResponse.code


class Lock(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Deletes a lock id associated with a user\'s account',
        parameters=[DeleteUserLockArgs.schema],
        responseClass=UserLockResponse.__name__,
        responseMessages=[UserLockResponse.description],
        tags=['Locks'],
    )
    @use_kwargs(DeleteUserLockArgs.resource_fields, locations=("json", "form"))
    @marshal_with_parser(UserLockResponse)
    @record_history(state_changes={
        UserLockResponse.code: StateChange.USER_LOCK_ADDED
    })
    def delete(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)
        result = user_lock_manager.delete_user_lock(uid, lock_id)
        return result, UserLockResponse.code
