from flask_restful import fields

from parsers.parser_utils import swagger_output_model


class classproperty(property):
    '''Subclass of property to make classmethod properties possible'''

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class ResponseBase(object):
    resource_fields = {}
    required = []
    code = 200
    description = 'A successful JSON response'


@swagger_output_model
class AdminLocksResponse(ResponseBase):
    resource_fields = {
        'id': fields.String(),
        'status': fields.String(),
        'nickname': fields.String(),
        'createdAt': fields.String(attribute="created_at")
    }
    required = ['id', 'status', 'nickname', 'created_at']
    code = 200
    description = 'A lock response'


@swagger_output_model
class LockPasswordResponse(ResponseBase):
    resource_fields = {
        'id': fields.String(),
        'status': fields.String(),
        'type': fields.String(),
        'createdAt': fields.String(attribute="created_at"),
        'expires': fields.String()
    }
    required = ['id', 'status', 'nickname', 'createdAt', 'type']
    code = 200
    description = 'A password response'


@swagger_output_model
class LockPasswordsResponse(ResponseBase):
    resource_fields = {
        'otp': fields.List(fields.Nested(LockPasswordResponse.resource_fields)),
        'permanent': fields.List(fields.Nested(LockPasswordResponse.resource_fields)),
    }
    required = ['otp', 'permanent']
    code = 200
    description = 'A response of the user\'s passwords'


@swagger_output_model
class UserResponse(ResponseBase):
    resource_fields = {
        'id': fields.String(attribute='id'),
        'email': fields.String(attribute='email'),
        'displayName': fields.String(attribute='name'),
    }
    required = ['id', 'email', 'displayName']
    code = 200
    description = 'A user response'


@swagger_output_model
class UserLockResponse(ResponseBase):
    resource_fields = {
        'ownedLockIds': fields.List(fields.String()),
    }
    required = ['ownedLockIds']
    code = 200
    description = 'A response of the user\'s owned locks'


@swagger_output_model
class UserLockStatusResponse(ResponseBase):
    resource_fields = {
        'status': fields.String()
    }
    required = ['status']
    code = 200
    description = 'A response of a lock\'s status belonging to a user'
