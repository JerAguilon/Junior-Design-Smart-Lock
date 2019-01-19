from webargs import fields
from parsers.enum_field import EnumField

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
