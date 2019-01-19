from flask import jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from utils.decorators import authorize
from document_templates.lock import Lock
from managers import lock_manager
from parsers.parsers import POST_LOCKS_ARGS
from parsers.parser_utils import webargs_to_doc

class Locks(Resource):
    method_decorators = [authorize(admin=True)]

    @swagger.operation(
        notes='Creates a lock given an admin id token',
        parameters=webargs_to_doc(POST_LOCKS_ARGS)
    )
    @use_kwargs(POST_LOCKS_ARGS, locations=("json", "form"))
    def post(self, uid, user, **args):
        lock = Lock.build(args)
        result = lock_manager.add_lock(lock)
        return jsonify(result)
