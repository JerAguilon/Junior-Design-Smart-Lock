from flask import Blueprint, request

from document_templates.user import User
from managers import user_manager

users_routes = Blueprint('users_routes', __name__)

@users_routes.route('/api/v1/user/', methods=['POST'])
def user():
    user = User.build(request.form)
    user_manager.create_or_update_user(user)
