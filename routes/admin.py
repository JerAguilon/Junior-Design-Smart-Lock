from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.lock import Lock
from managers import lock_manager
from security import security_utils
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import PostLocksArgs
from parsers.response_parsers import AdminLocksResponse
from utils.decorators import authorize


class Locks(Resource):
    """
    An admin api token is required in order to use this route.
    This is used to register new lock devices to the database.
    """
    method_decorators = [authorize(admin=True)]

    @swagger.operation(
        notes='Creates a lock given an admin id token',
        parameters=[PostLocksArgs.schema],
        responseClass=AdminLocksResponse.__name__,
        responseMessages=[AdminLocksResponse.description],
        tags=['Admin']
    )
    @marshal_with_parser(AdminLocksResponse)
    @use_kwargs(PostLocksArgs.resource_fields, locations=("json", "form"))
    def post(self, uid, user, **args):
        args['secret'] = security_utils.hash_password(args['secret'])
        lock = Lock.build(args)
        lock_manager.add_lock(lock)
        return lock, AdminLocksResponse.code
