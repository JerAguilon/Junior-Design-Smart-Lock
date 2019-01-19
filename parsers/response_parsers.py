from flask_restful import fields
from flask_restful_swagger import swagger

@swagger.model
class UserResponse:
    resource_fields = {
        'id': fields.String(attribute='id'),
        'email': fields.String(attribute='email'),
        'displayName': fields.String(attribute='name'),
    }
