from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from managers import lock_manager
from parsers.parser_utils import marshal_with_parser, webargs_to_doc
from parsers.request_parsers import PutLockStatusArgs, PUT_LOCK_STATUS_ARGS
from parsers.response_parsers import UserLockStatusResponse
from security import security_utils
from utils.decorators import authorize


class LockPassword(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Gets information on a lock password',
    )
    def get(self):
        return {}, 200

    @swagger.operation(
        notes='Changes a password',
    )
    def put(self):
        return {}, 200


class LockPasswords(Resource):
    @swagger.operation(
        notes='Adds a password',
    )
    def get(self):
        return {}, 200


class LockStatus(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Updates a lock status',
        parameters=[
            {
                'name': 'body',
                'dataType': PutLockStatusArgs.name,
                'paramType': 'PutLockStatusArgs'
            }
        ],
        responseClass=UserLockStatusResponse.name,
        responseMessages=[UserLockStatusResponse.description],
    )
    @use_kwargs(PUT_LOCK_STATUS_ARGS, locations=("json", "form"))
    @marshal_with_parser(UserLockStatusResponse)
    def put(self, uid, user, **args):
        lock_id = args['lock_id']
        security_utils.verify_lock_ownership(uid, lock_id)
        return lock_manager.change_lock_status(lock_id, args.get('status')), UserLockStatusResponse.code

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
    @marshal_with_parser(UserLockStatusResponse)
    def get(self, uid, user, lock_id):
        security_utils.verify_lock_ownership(uid, lock_id)
        return lock_manager.get_lock_status(lock_id), UserLockStatusResponse.code
