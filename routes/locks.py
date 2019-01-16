from flask import Blueprint, request, jsonify

from utils.decorators import authorize
from document_templates.user_locks import UserLocks
from managers import user_lock_manager

locks_routes = Blueprint('locks_routes', __name__)

@locks_routes.route('/api/v1/user_locks', methods=['POST', 'GET'])
@authorize()
def user_locks(uid, user):
    if request.method ==  'POST':
        user_locks = UserLocks.build(request.form)
        result = user_lock_manager.create_or_update_user_lock(uid, user_locks, should_overwrite=False)
        return jsonify(result)

    if request.method == 'GET':
        return jsonify(user_lock_manager.get_user_locks(uid))
