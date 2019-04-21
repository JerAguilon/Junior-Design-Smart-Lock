from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.history import Event, StateChange
from managers import lock_manager, password_manager, history_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import (
    DeleteHardwarePasswordsArgs,
    PostHardwareEventArgs,
    PutHardwareLockStatusArgs,
)
from parsers.response_parsers import (
    SyncLockPasswordsResponse,
    UserLockStatusResponse
)
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


class HardwareLockSync(Resource):
    method_decorators = [authorize_hardware()]

    @swagger.operation(
        notes='Syncs passwords locally',
        responseClass=SyncLockPasswordsResponse.__name__,
        responseMessages=[SyncLockPasswordsResponse.description],
        tags=['Hardware'],
    )
    @marshal_with_parser(SyncLockPasswordsResponse)
    def get(self, lock_id, **kwargs):
        return (
            password_manager.get_passwords(lock_id),
            SyncLockPasswordsResponse.code
        )


class HardwareEvents(Resource):
    method_decorators = [authorize_hardware()]

    @swagger.operation(
        notes=('Adds a hardware event to the server. The event can be '
               'one of {}.'.format([s.value for s in StateChange])),
        parameters=[PostHardwareEventArgs.schema],
        tags=['Hardware'],
    )
    @use_kwargs(
        PostHardwareEventArgs.resource_fields,
        locations=("json", "form")
    )
    def post(self, lock_id, **kwargs):
        if kwargs.get('createdAt') == -1:
            kwargs['createdAt'] = None

        event = Event(
            status=kwargs['event'],
            user_id="N/A",
            lock_id=lock_id,
            endpoint="N/A",
            created_at=kwargs.get('createdAt'),
        )
        history_manager.add_event(event)
        return {}, 200


class HardwarePasswordUpdates(Resource):
    method_decorators = [authorize_hardware()]

    @swagger.operation(
        notes='Removes passwords given a list of valid password ids',
        parameters=[DeleteHardwarePasswordsArgs.schema],
        tags=['Hardware'],
    )
    @use_kwargs(
        DeleteHardwarePasswordsArgs.resource_fields,
        locations=("json", "form")
    )
    def delete(self, lock_id, **kwargs):
        for password_id in kwargs['passwordIds']:
            password_manager.remove_password_by_id(lock_id, password_id)

        return {}, 200
