from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from managers import lock_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import (
    PutHardwareLockStatusArgs
)
from parsers.response_parsers import UserLockStatusResponse
from utils.decorators import authorize_hardware


class HardwareLockStatus(Resource):
    method_decorators = [authorize_hardware()]

    @swagger.operation(
        notes='Updates a lock status',
        parameters=[PutHardwareLockStatusArgs.schema],
        responseClass=UserLockStatusResponse.__name__,
        responseMessages=[UserLockStatusResponse.description],
        tags=['Hardware'],
    )
    @use_kwargs(
        PutHardwareLockStatusArgs.resource_fields,
        locations=("json", "form")
    )
    @marshal_with_parser(UserLockStatusResponse)
    def put(self, lock_id, status, **args):
        result = lock_manager.change_lock_status(
            lock_id, status
        ), UserLockStatusResponse.code
        return result

    @swagger.operation(
        notes='Gets the lock status',
        responseClass=UserLockStatusResponse.__name__,
        responseMessages=[UserLockStatusResponse.description],
        tags=['Hardware'],
    )
    @marshal_with_parser(UserLockStatusResponse)
    def get(self, lock_id, **kwargs):
        return lock_manager.get_lock_status(
            lock_id), UserLockStatusResponse.code
