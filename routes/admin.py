from flask import Blueprint, request, jsonify

from utils.decorators import authorize
from document_templates.lock import Lock
from managers import lock_manager

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/api/v1/admin/locks', methods=['POST'])
@authorize(admin=True)
def locks(uid, user):
    lock = Lock.build(request.form)
    result = lock_manager.add_lock(lock)
    return jsonify(result)
