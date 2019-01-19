from flask import jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates import user
from managers import user_manager
from parsers.parser_utils import webargs_to_doc
from parsers.request_parsers import POST_USER_ARGS
from utils.decorators import authorize

class User(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Returns user information',
        parameters=[]
    )
    def get(self, uid, user_dict):
        return jsonify(user_manager.get_user(uid))

    @swagger.operation(
        notes='Returns user information',
        parameters=webargs_to_doc(POST_USER_ARGS)
    )
    @use_kwargs(POST_USER_ARGS)
    def post(self, uid, user_dict, **kwargs):
        new_user = user.User.build(kwargs)
        user_manager.create_or_update_user(new_user)
        return jsonify(user.serialize())

