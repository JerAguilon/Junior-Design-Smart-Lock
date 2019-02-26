from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.history import StateChange
from document_templates.lock import LockStatus as LockStatusEnum
from document_templates.password import Password, PasswordType
from managers import lock_manager, password_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import (
    GetLockPasswordMetadataArgs,
    PostLockPasswordsArgs,
    PutLockPasswordArgs,
    PutLockStatusArgs)
from parsers.response_parsers import (
    LockPasswordsResponse,
    LockPasswordResponse,
    UserLockStatusResponse,
    PutUserLockStatusResponse
)
from security import security_utils
from utils.decorators import authorize, record_history
from utils.exceptions import AuthorizationException


PASSWORD_INFO = ("Passwords are passed as arguments "
                 "to change the status or sensitive metadata of a lock. "
                 "In addition, the user needs to own the lock as well")


class LockPassword(Resource):

    method_decorators = [authorize()]

    @swagger.operation(
        notes='Gets metadata on a lock password. ' + PASSWORD_INFO,
        tags=['Password Management'],
        responseClass=LockPasswordResponse.__name__,
        responseMessages=[LockPasswordResponse.description],
    )
    @use_kwargs(
        GetLockPasswordMetadataArgs.resource_fields,
        locations=(
            "json",
            "form"))
    @marshal_with_parser(LockPasswordResponse)
    def get(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        password_id = kwargs['passwordId']
        security_utils.verify_lock_ownership(uid, lock_id)
        return (password_manager.get_password_metadata(lock_id, password_id),
                LockPasswordResponse.code)

    @swagger.operation(
        notes='Changes a password. ' + PASSWORD_INFO,
        tags=['Password Management'],
        parameters=[PutLockPasswordArgs.schema],
        responseClass=LockPasswordResponse.__name__,
        responseMessages=[LockPasswordResponse.description],
    )
    @use_kwargs(
        PutLockPasswordArgs.resource_fields,
        locations=(
            "json",
            "form"))
    @marshal_with_parser(LockPasswordResponse)
    @record_history(state_changes={
        LockPasswordResponse.code: StateChange.PASSWORD_METADATA_CHANGED
    })
    def put(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        password_id = kwargs['passwordId']

        # TODO(jeremy): roll this into an update request object
        update_args = self._build_update_args(kwargs)

        result = password_manager.update_password(
            lock_id,
            password_id,
            update_args,
        )
        return result, LockPasswordResponse.code

    def _build_update_args(self, kwargs):
        if 'password' in kwargs:
            kwargs['password'] = security_utils.hash_password(
                kwargs['password'])

        update_args = {}
        for arg in list(PutLockPasswordArgs.resource_fields.keys()):
            if arg in kwargs:
                update_args[arg] = kwargs[arg]
        return update_args


class LockPasswords(Resource):

    method_decorators = [authorize()]

    @swagger.operation(
        notes='Gets metadata about a lock\'s passwords. ' + PASSWORD_INFO,
        tags=['Password Management'],
        responseClass=LockPasswordsResponse.__name__,
        responseMessages=[LockPasswordsResponse.description],
    )
    @marshal_with_parser(LockPasswordsResponse)
    def get(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)

        result = password_manager.get_passwords_metadata(lock_id), 200
        return result

    @swagger.operation(
        notes='Adds a password to a lock. ' + PASSWORD_INFO,
        tags=['Password Management'],
        parameters=[PostLockPasswordsArgs.schema],
        responseClass=LockPasswordResponse.__name__,
        responseMessages=[LockPasswordResponse.description],
    )
    @use_kwargs(
        PostLockPasswordsArgs.resource_fields,
        locations=(
            "json",
            "form"))
    @record_history(state_changes={
        LockPasswordResponse.code: StateChange.PASSWORD_CREATED
    })
    @marshal_with_parser(LockPasswordResponse)
    def post(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)

        kwargs['password'] = security_utils.hash_password(kwargs['password'])

        password = Password.build(kwargs)
        return (password_manager.add_password(lock_id, password),
                LockPasswordResponse.code)


LOCK_STATUS_PUT_NOTES = ("Updates a lock status. If an inputted password "
                         "is removed (as with OTP passwords), then the JSON "
                         "payload will contain inputedPasswordDisabled: true")


class LockStatus(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes=LOCK_STATUS_PUT_NOTES,
        parameters=[PutLockStatusArgs.schema],
        responseClass=PutUserLockStatusResponse.__name__,
        responseMessages=[PutUserLockStatusResponse.description],
        tags=['Locks'],
    )
    @use_kwargs(PutLockStatusArgs.resource_fields, locations=("json", "form"))
    @marshal_with_parser(PutUserLockStatusResponse)
    @record_history(state_changes={
        PutUserLockStatusResponse.code: StateChange.LOCK_STATE_CHANGED
    })
    def put(self, uid, user, **args):
        lock_id = args['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)

        # TODO: refactor this into something less hacky than enum matching
        if args.get('status') != LockStatusEnum.OPEN_REQUESTED:
            error_message = 'Users cannot set the lock to open or closed. ' + \
                'Open or close the vault to do so.'
            raise AuthorizationException(error_message)

        was_lock_removed = False
        found_password = security_utils.verify_password(
            lock_id, args.get('password'))
        if found_password.type == PasswordType.OTP:
            password_manager.remove_password(lock_id, found_password)
            was_lock_removed = True

        result = lock_manager.change_lock_status(
            lock_id, args.get('status'), was_lock_removed
        ), PutUserLockStatusResponse.code

        return result

    @swagger.operation(
        notes='Gets the lock status of a user owned lock',
        responseClass=UserLockStatusResponse.__name__,
        responseMessages=[UserLockStatusResponse.description],
        tags=['Locks'],
    )
    @marshal_with_parser(UserLockStatusResponse)
    def get(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)
        return lock_manager.get_lock_status(
            lock_id), UserLockStatusResponse.code
