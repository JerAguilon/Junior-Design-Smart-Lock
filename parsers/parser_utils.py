from flask_restful import marshal
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


def marshal_with_parser(resp_parser):
    def actual_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                import pdb; pdb.set_trace()
                result, code = function(*args, **kwargs)
                marshaled_result = marshal(result, resp_parser.resource_fields)

                missing_fields = [
                    req for req in resp_parser.required if
                    (req not in marshaled_result or marshaled_result[req] is None)
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
