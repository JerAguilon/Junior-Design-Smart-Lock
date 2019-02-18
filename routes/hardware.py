from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from managers import lock_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import (
    HardwarePutLockStatusArgs
)
from parsers.response_parsers import UserLockStatusResponse
from security import security_utils
from utils.decorators import authorize_hardware


class LockStatus(Resource):
    method_decorators = [authorize_hardware()]

    @swagger.operation(
        notes=None,
        parameters=[HardwarePutLockStatusArgs.schema],
        responseClass=UserLockStatusResponse.__name__,
        responseMessages=[UserLockStatusResponse.description],
        tags=['Locks'],
    )
    @use_kwargs(HardwarePutLockStatusArgs.resource_fields, locations=("json", "form"))
    @marshal_with_parser(UserLockStatusResponse)
    def put(self, lock_id, mac_address, status, **args):
        security_utils.update_lock_status(lock_id, status)
        result = lock_manager.change_lock_status(
            lock_id, status
        ), UserLockStatusResponse.code
        return result

    @swagger.operation(
        notes='Gets the lock status of a user owned lock',
        responseClass=UserLockStatusResponse.__name__,
        responseMessages=[UserLockStatusResponse.description],
        tags=['Locks'],
    )
    @marshal_with_parser(UserLockStatusResponse)
    def get(self, **kwargs):
        lock_id = kwargs['lockId']
        return lock_manager.get_lock_status(
            lock_id), UserLockStatusResponse.code
