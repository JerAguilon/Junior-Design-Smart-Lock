from flask_restful import Resource
from flask_restful_swagger import swagger

from document_templates.user import User as UserTemplate
from managers import user_manager
from parsers.parser_utils import marshal_with_parser
from parsers.response_parsers import UserResponse
from utils.decorators import authorize


class User(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Returns user information',
        parameters=[],
        responseClass=UserResponse.name,
        responseMessages=[UserResponse.description],
        tags=['Users'],
    )
    @marshal_with_parser(UserResponse)
    def get(self, uid, user_dict):
        found_user = UserTemplate.from_database(
            uid, user_manager.get_user(uid))
        return found_user, UserResponse.code

    @swagger.operation(
        notes='Returns user information',
        parameters=[],
        responseClass=UserResponse.name,
        responseMessages=[UserResponse.description],
        tags=['Users'],
    )
    @marshal_with_parser(UserResponse)
    def post(self, uid, user_dict):

        new_user = {
            'email': user_dict['email'],
            'name': user_dict.get('displayName', '')
        }
        new_user['id'] = uid
        new_user_template = UserTemplate.build(new_user)
        user_manager.create_or_update_user(uid, new_user_template)
        return new_user, UserResponse.code
