from flask import Blueprint, request, jsonify

from utils.decorators import authorize, use_request_form
from document_templates.user_locks import UserLocks
from managers import lock_manager, user_lock_manager
from security import security_utils

locks_routes = Blueprint('locks_routes', __name__)

@locks_routes.route('/api/v1/userLocks', methods=['POST', 'GET'])
@authorize()
def user_locks(uid, user):
    if request.method ==  'POST':
        user_locks = UserLocks.build(request.form)
        result = user_lock_manager.create_or_update_user_lock(uid, user_locks, should_overwrite=False)
        return jsonify(result)

    if request.method == 'GET':
        return jsonify(user_lock_manager.get_user_locks(uid))

@locks_routes.route('/api/v1/locks/<lock_id>/lockStatus', methods=['PUT', 'GET'])
@authorize()
@use_request_form()
def user_lock_status(request_form, uid, user, lock_id):
    security_utils.verify_lock_ownership(uid, lock_id)

    if request.method ==  'PUT':
        return jsonify(lock_manager.change_lock_status(lock_id, request_form.get('status')))

    if request.method == 'GET':
        return jsonify(lock_manager.get_lock_status(lock_id))

