from flask_restful import Resource
from flask_restful_swagger import swagger
from webargs.flaskparser import use_kwargs

from document_templates.lock import Password
from document_templates.lock import LockStatus as LockStatusEnum
from managers import lock_manager, password_manager
from parsers.parser_utils import marshal_with_parser
from parsers.request_parsers import (
    GetLockPasswordMetadataArgs, PostLockPasswordsArgs, PutLockStatusArgs)
from parsers.response_parsers import (
    LockPasswordsResponse, LockPasswordResponse, UserLockStatusResponse)
from security import security_utils
from utils.decorators import authorize
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
    def get(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        password_id = kwargs['passwordId']
        security_utils.verify_lock_ownership(uid, lock_id)
        return (password_manager.get_password_metadata(lock_id, password_id),
                LockPasswordResponse.code)

    @swagger.operation(
        notes='Changes a password. ' + PASSWORD_INFO,
        tags=['Password Management'],
        responseClass=LockPasswordResponse.__name__,
        responseMessages=[LockPasswordResponse.description],
    )
    def put(self):
        return {}, 200


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
    @marshal_with_parser(LockPasswordResponse)
    def post(self, uid, user, **kwargs):
        lock_id = kwargs['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)

        kwargs['password'] = security_utils.hash_password(kwargs['password'])

        password = Password.build(kwargs)
        return (password_manager.add_password(lock_id, password),
                LockPasswordResponse.code)


class LockStatus(Resource):
    method_decorators = [authorize()]

    @swagger.operation(
        notes='Updates a lock status',
        parameters=[PutLockStatusArgs.schema],
        responseClass=UserLockStatusResponse.__name__,
        responseMessages=[UserLockStatusResponse.description],
        tags=['Locks'],
    )
    @use_kwargs(PutLockStatusArgs.resource_fields, locations=("json", "form"))
    @marshal_with_parser(UserLockStatusResponse)
    def put(self, uid, user, **args):
        lock_id = args['lockId']
        security_utils.verify_lock_ownership(uid, lock_id)

        # TODO: refactor this into something less hacky than enum matching
        if args.get('status') == LockStatusEnum.OPEN_REQUESTED:
            security_utils.verify_password(lock_id, args.get('password'))
        else:
            error_message = 'Users cannot set the lock to open or closed. ' + \
                'Open or close the vault to do so.'
            raise AuthorizationException(error_message)

        return lock_manager.change_lock_status(
            lock_id, args.get('status')), UserLockStatusResponse.code

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
