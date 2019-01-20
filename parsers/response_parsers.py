from flask_restful import fields
from flask_restful_swagger import swagger

from parsers.parser_utils import swagger_output_model


@swagger.model
@swagger_output_model
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
@swagger_output_model
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
@swagger_output_model
class UserResponse(object):
    resource_fields = {
        'id': fields.String(attribute='id'),
        'email': fields.String(attribute='email'),
        'displayName': fields.String(attribute='name'),
    }
    required = ['id', 'email', 'displayName']
    code = 200


@swagger.model
@swagger_output_model
class UserLockResponse(object):
    resource_fields = {
        'ownedLockIds': fields.List(fields.String()),
    }
    required = ['ownedLockIds']
    code = 200


@swagger.model
@swagger_output_model
class UserLockStatusResponse(object):
    resource_fields = {
        'status': fields.String()
    }
    required = ['status']
    code = 200
