from flask_restful import marshal
from flask_restful import fields as restful_fields
from flask_restful_swagger import swagger
from functools import wraps
from webargs import fields

from parsers.enum_field import EnumField
from utils.exceptions import AppException, ValidationException

DATA_TYPE_MAP = {
    fields.Str: "string",
    EnumField: "string",
    fields.Int: "int",
    fields.DelimitedList: "array"
}

WEBARGS_TO_RESTFUL_MAP = {
    fields.Str: restful_fields.String,
    EnumField: restful_fields.String,
    fields.Int: restful_fields.Integer,
    fields.DelimitedList: restful_fields.List,
}


def _add_data_type(instance, entry):
    entry["dataType"] = DATA_TYPE_MAP[instance.__class__]
    if instance.__class__ == fields.DelimitedList:
        entry["items"] = {"type": DATA_TYPE_MAP[instance.container.__class__]}
    if instance.__class__ == EnumField:
        enum_values = [f.value for f in instance.enum]
        entry["enum"] = enum_values
        if entry["description"][-1] != '.':
            entry["description"] += '.'
        entry["description"] += ' One of {}'.format(enum_values)


def swagger_input_model(cls):
    def _transform_resource_fields(cls):
        resource_fields = {}
        required = []

        for key, value in cls.resource_fields.items():
            # skip all URL parameters
            if value.metadata.get('location', '') == 'view_args':
                continue

            if value.required:
                required.append(key)

            restful_field = WEBARGS_TO_RESTFUL_MAP[value.__class__]
            args = []
            if hasattr(value, 'container'):
                args.append(WEBARGS_TO_RESTFUL_MAP[value.container.__class__])
            resource_fields[key] = restful_field(*args)

        return resource_fields, required

    resource_fields, required = _transform_resource_fields(cls)

    class SwaggerInputSingleton(cls):
        def __init__(self, resource_fields={}, required=[]):
            self.__doc__ = cls.__doc__
            self.__name__ = cls.__name__
            self._resource_fields = resource_fields
            self._required = required

        @property
        def resource_fields(self):
            return self._resource_fields

        @property
        def required(self):
            return self._required

        @property
        def name(self):
            return cls.__name__

    schema = {
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            "$ref": "#/definitions/{}".format(cls.__name__),
        },
        'dataType': cls.__name__,
        'paramType': 'body'
    }
    cls.schema = schema

    swagger.model(SwaggerInputSingleton(resource_fields, required))
    return cls


def swagger_output_model(cls):

    class SwaggerOutputSingleton(cls):
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
    swagger.add_model(SwaggerOutputSingleton())
    return cls


def marshal_with_parser(resp_parser):
    def actual_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result, code = function(*args, **kwargs)
                marshaled_result = marshal(result, resp_parser.resource_fields)

                missing_fields = [
                    req for req in resp_parser.required if
                    (req not in marshaled_result
                        or marshaled_result[req] is None)
                ]
                if len(missing_fields) > 0:
                    raise ValidationException(
                        "Response is missing required field(s): {}".format(
                            missing_fields
                        )
                    )
                return marshaled_result, code
            except AppException as e:
                return e.to_dict(), e.status_code

        return wrapper
    return actual_decorator


def webargs_to_doc(args):
    output = []
    for key, value in args.items():
        new_entry = {
            'name': key,
            'description': value.metadata.get('description', ''),
            'required': value.required,
            'paramType': 'path' if value.metadata.get('location') else 'body'
        }
        _add_data_type(value, new_entry)
        output.append(new_entry)
    return output
