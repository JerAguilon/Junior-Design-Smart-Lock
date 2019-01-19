from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.lock import Lock
from managers import lock_manager
from parsers.parser_utils import webargs_to_doc
from parsers.request_parsers import POST_LOCKS_ARGS
from parsers.response_parsers import AdminLocksResponse
from utils.decorators import authorize


class Locks(Resource):
    method_decorators = [authorize(admin=True)]

    @swagger.operation(
        notes='Creates a lock given an admin id token',
        parameters=webargs_to_doc(POST_LOCKS_ARGS),
        responseClass=AdminLocksResponse.__name__,
        responseMessages=[AdminLocksResponse.description],
    )
    @marshal_with(AdminLocksResponse.resource_fields)
    @use_kwargs(POST_LOCKS_ARGS, locations=("json", "form"))
    def post(self, uid, user, **args):
        lock = Lock.build(args)
        lock_manager.add_lock(lock)
        return lock, AdminLocksResponse.code
