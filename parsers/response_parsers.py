from flask_restful import fields
from flask_restful_swagger import swagger


class overridable(property):
    """Subclass property to make classmethod properties possible"""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class ResponseBase(object):
    @overridable
    @classmethod
    def resource_fields(cls):
        return {}

    @overridable
    @classmethod
    def code(cls):
        return 200

    @overridable
    @classmethod
    def required(cls):
        return []

    @overridable
    @classmethod
    def message(cls):
        return 'A {} object'.format(cls.__name__)

    @overridable
    @classmethod
    def description(cls):
        return {'code': cls.code, 'message': cls.message}


@swagger.model
class AdminLocksResponse(ResponseBase):
    resource_fields = {
        'id': fields.String(),
        'status': fields.String(),
        'nickname': fields.String(),
        'created_at': fields.String(attribute="created_at")
    }
    required=['id', 'status', 'nickname', 'created_at']
    code = 200


@swagger.model
class UserResponse(ResponseBase):
    resource_fields = {
        'id': fields.String(attribute='id'),
        'email': fields.String(attribute='email'),
        'displayName': fields.String(attribute='name'),
    }
    required=['id', 'email', 'displayName']
    code = 200

@swagger.model
class UserLockResponse(ResponseBase):
    resource_fields = {
        'ownedLockIds': fields.List(fields.String()),
    }
    required=['ownedLockIds']
    code = 200

@swagger.model
class UserLockStatusResponse(ResponseBase):
    resource_fields = {
        'status': fields.String()
    }
    required=['status']
    code = 200
