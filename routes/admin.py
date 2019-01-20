from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.lock import Lock
from managers import lock_manager
from parsers.parser_utils import marshal_with_parser, webargs_to_doc
from parsers.request_parsers import POST_LOCKS_ARGS
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
        parameters=webargs_to_doc(POST_LOCKS_ARGS),
        responseClass=AdminLocksResponse.__name__,
        responseMessages=[AdminLocksResponse.description],
    )
    @marshal_with_parser(AdminLocksResponse)
    @use_kwargs(POST_LOCKS_ARGS, locations=("json", "form"))
    def post(self, uid, user, **args):
        lock = Lock.build(args)
        lock_manager.add_lock(lock)
        return lock, AdminLocksResponse.code
