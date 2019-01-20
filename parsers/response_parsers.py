from flask_restful import fields
from flask_restful_swagger import swagger


def swagger_generator(cls):
    class SwaggerWrapperSingleton(cls):
        def __init__(self):
            self.__doc__ = cls.__doc__
            self.__name__ = cls.__name__

        _resource_fields = cls.resource_fields if hasattr(
            cls, 'resource_fields') else {}
        _code = cls.code if hasattr(cls, 'code') else 200
        _message = cls.message if hasattr(
            cls, 'message') else 'A {} object'.format(
            cls.__name__)
        _required = cls.required if hasattr(cls, 'required') else True

        @property
        def resource_fields(self):
            return self._resource_fields

        @property
        def code(self):
            return self._code

        @property
        def required(self):
            return self._required

        @property
        def message(self):
            self._message

        @property
        def description(self):
            return {'code': self._code, 'message': self._message}

        @property
        def name(self):
            return cls.__name__

    return SwaggerWrapperSingleton()


@swagger.model
@swagger_generator
class AdminLocksResponse(object):
    resource_fields = {
        'id': fields.String(),
        'status': fields.String(),
        'nickname': fields.String(),
        'created_at': fields.String(attribute="created_at")
    }
    required = ['id', 'status', 'nickname', 'created_at']
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

