from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.history import StateChange
from managers import history_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import GetLockHistoryArgs
from parsers.response_parsers import LockHistoryResponse
from security import security_utils
from utils.decorators import authorize


HISTORY_INFO = (
    "Resource that lets users retrieve events given a lock id. "
    "See `LockEvent` for the schema for each response. Note that "
    "status can be one of {}."
).format(
    [s.value for s in StateChange]
)


class LockHistory(Resource):

    method_decorators = [authorize()]

    @swagger.operation(
        notes=HISTORY_INFO,
        tags=['History'],
        responseClass=LockHistoryResponse.__name__,
        responseMessages=[LockHistoryResponse.description],
    )
    @use_kwargs(
        GetLockHistoryArgs.resource_fields,
        locations=(
            "json",
            "form"))
    @marshal_with_parser(LockHistoryResponse)
    def get(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)
        events = history_manager.get_events_from_lock_id(lock_id)
        return ({'events': events},
                LockHistoryResponse.code)
