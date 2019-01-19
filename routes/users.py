from flask import jsonify
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.user import User as UserTemplate
from managers import user_manager
from parsers.parser_utils import webargs_to_doc
from parsers.request_parsers import POST_USER_ARGS
from parsers.response_parsers import UserResponse
from utils.decorators import authorize

class User(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Returns user information',
        response_class=UserResponse.__name__,
        parameters=[]
    )
    @marshal_with(UserResponse.resource_fields)
    def get(self, uid, user_dict):
        found_user = UserTemplate.from_database(uid, user_manager.get_user(uid))
        return found_user
        return jsonify(user_manager.get_user(uid))

    @swagger.operation(
        notes='Returns user information',
        parameters=webargs_to_doc(POST_USER_ARGS)
    )
    @use_kwargs(POST_USER_ARGS)
    def post(self, uid, user_dict, **kwargs):
        args = kwargs
        args['id'] = kwargs
        new_user = UserTemplate.build(kwargs)
        user_manager.create_or_update_user(new_user)
        return jsonify(new_user.serialize())

