from flask import Blueprint, request, jsonify

from utils.decorators import authorize
from document_templates.user import User
from managers import user_manager

users_routes = Blueprint('users_routes', __name__)

@users_routes.route('/api/v1/user', methods=['GET', 'POST'])
@authorize
def user(uid, user):
    if request.method ==  'POST':
        user = User.build(request.form)
        user_manager.create_or_update_user(user)
        return jsonify(user.serialize())

    if request.method == 'GET':
        return jsonify(user_manager.get_user(uid))
