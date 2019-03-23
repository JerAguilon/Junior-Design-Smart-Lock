from flask_restful import fields
from flask_restful_swagger import swagger

from document_templates.history import StateChange
from document_templates.password import PasswordType, PasswordDays
from document_templates.lock import LockStatus
from parsers.parser_utils import swagger_output_model
from utils.exceptions import AppException


class EnumField(fields.String):
    def __init__(self, enum_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_type = enum_type

    def format(self, enum):
        if not isinstance(enum, self.enum_type):
            raise AppException("Response object failed to serialize")
        return enum.value


class TimezoneField(fields.String):
    def format(self, value):
        return value.zone


@swagger.model
@swagger_output_model
class AdminLocksResponse(object):
    resource_fields = {
        'id': fields.String(),
        'status': EnumField(LockStatus),
        'timezone': TimezoneField(),
        'nickname': fields.String(),
        'createdAt': fields.Integer(attribute="created_at")
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
        'createdAt': fields.Integer(
            attribute="created_at"),
        'activeDays': fields.List(
            EnumField(PasswordDays),
            attribute="active_days"),
        'activeTimes': fields.List(
            fields.String(),
            attribute="activeDays")
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


@swagger.model
@swagger_output_model
class LockEvent(object):
    resource_fields = {
        'userId': fields.String(attribute='user_id'),
        'lockId': fields.String(attribute='lock_id'),
        'endpoint': fields.String(),
        'status': EnumField(StateChange),
        'createdAt': fields.Integer(attribute='created_at'),
    }
    required = ['userId', 'lockId', 'endpoint', 'status', 'createdAt']


@swagger.model
@swagger_output_model
class LockHistoryResponse(object):
    resource_fields = {
        'events': fields.List(
            fields.Nested(LockEvent.resource_fields)
        )
    }

    required = ['events']
    code = 200
