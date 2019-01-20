from flask_restful import fields
from flask_restful_swagger import swagger

from parsers.parser_utils import swagger_generator


@swagger.model
@swagger_generator
class AdminLocksResponse(object):
    resource_fields = {
        'id': fields.String(),
        'status': fields.String(),
        'nickname': fields.String(),
        'createdAt': fields.String(attribute="created_at")
    }
    required = ['id', 'status', 'nickname', 'created_at']
    code = 200


@swagger.model
@swagger_generator
class LockPasswordResponse(object):
    resource_fields = {
        'id': fields.String(),
        'status': fields.String(),
        'type': fields.String(),
        'createdAt': fields.String(attribute="created_at"),
        'expires': fields.String()
    }
    required = ['id', 'status', 'nickname', 'createdAt', 'type']
    code = 200


@swagger.model
@swagger_generator
class UserResponse(object):
    resource_fields = {
        'id': fields.String(attribute='id'),
        'email': fields.String(attribute='email'),
        'displayName': fields.String(attribute='name'),
    }
    required = ['id', 'email', 'displayName']
    code = 200


@swagger.model
@swagger_generator
class UserLockResponse(object):
    resource_fields = {
        'ownedLockIds': fields.List(fields.String()),
    }
    required = ['ownedLockIds']
    code = 200


@swagger.model
@swagger_generator
class UserLockStatusResponse(object):
    resource_fields = {
        'status': fields.String()
    }
    required = ['status']
    code = 200
