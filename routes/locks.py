from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.user_locks import UserLocks
from managers import user_lock_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import PostUserLockArgs
from parsers.response_parsers import UserLockResponse
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
        return user_lock_manager.get_user_locks(uid), UserLockResponse.code

    @swagger.operation(
        notes='Adds a valid lock id to a user\'s account',
        parameters=[PostUserLockArgs.schema],
        responseClass=UserLockResponse.name,
        responseMessages=[UserLockResponse.description],
    )
    @use_kwargs(PostUserLockArgs.resource_fields, locations=("json", "form"))
    @marshal_with_parser(UserLockResponse)
    def post(self, uid, user, **args):
        user_locks = UserLocks.build(args)
        result = user_lock_manager.create_or_update_user_lock(
            uid, user_locks, should_overwrite=False)
        return result, UserLockResponse.code
