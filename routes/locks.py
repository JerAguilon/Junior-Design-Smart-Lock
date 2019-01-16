from flask import Blueprint, request, jsonify

from utils.decorators import authorize
from document_templates.user import User
from managers import user_manager

locks_routes = Blueprint('locks_routes', __name__)

@locks_routes.route('/api/v1/lock', methods=['POST'])
@authorize
def lock(uid, user):
    if request.method ==  'POST':
        user = User.build(request.form)
        user_manager.create_or_update_user(user)
        return jsonify(user.serialize())

    if request.method == 'GET':
        return jsonify({'uid':uid, 'user':user})
        user = User.build(request.form)
        user_manager.create_or_update_user(user)
        return jsonify(user.serialize())
