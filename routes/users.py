from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from webargs.flaskparser import use_args

from document_templates.user import User
from managers import user_manager
from parsers.parsers import POST_USER_ARGS
from utils.decorators import authorize

users_routes = Blueprint('users_routes', __name__)

class User(Resource):
    method_decorators = [authorize()]

    def get(self, uid, user):
        return jsonify(user_manager.get_user(uid))

    def post(self, uid, user):
        user = User.build(request.form)
        user_manager.create_or_update_user(user)
        return jsonify(user.serialize())

api = Api(users_routes)
api.add_resource(User, "/api/v1/user")
