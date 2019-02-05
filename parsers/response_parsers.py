from flask_restful import fields
from flask_restful_swagger import swagger

from document_templates.lock import PasswordType
from utils.exceptions import AppException
from parsers.parser_utils import swagger_output_model


class EnumField(fields.Raw):
    def __init__(self, enum_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_type = enum_type

    def format(self, enum):
        if not isinstance(enum, self.enum_type):
            raise AppException("Response object failed to serialize")
        return enum.value


@swagger.model
@swagger_output_model
class AdminLocksResponse(object):
    resource_fields = {
        'id': fields.String(),
        'status': fields.String(),
        'nickname': fields.String(),
        'createdAt': fields.String(attribute="created_at")
    }
    required = ['id', 'status', 'nickname', 'createdAt']
    code = 200


@swagger.model
@swagger_output_model
class LockPasswordResponse(object):
    resource_fields = {
        'id': fields.String(),
        'type': EnumField(PasswordType),
        'expiration': fields.Integer(),
        'createdAt': fields.Integer(attribute="created_at")
    }
    required = ['id', 'createdAt', 'type']
    code = 200


@swagger.model
@swagger_output_model
class LockPasswordsResponse():
    resource_fields = {
        'otp': fields.List(
            fields.Nested(LockPasswordResponse.resource_fields)
        ),
        'permanent': fields.List(
            fields.Nested(LockPasswordResponse.resource_fields)
        ),
    }
    required = ['otp', 'permanent']
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
        'status': fields.String(),
    }
    required = ['status']
    code = 200


@swagger.model
@swagger_output_model
class PutUserLockStatusResponse(object):
    resource_fields = {
        'status': fields.String(),
        'providedPasswordDisabled': fields.Boolean()
    }
    required = ['status', 'providedPasswordDisabled']
    code = 200
