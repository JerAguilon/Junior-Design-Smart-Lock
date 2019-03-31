import os
import pytest

import bcrypt

from configparser import ConfigParser

from document_templates.lock import Lock
from document_templates.password import PasswordType, Password
from document_templates.user import User
from document_templates.user_locks import UserLocks
from firebase import firebase_config
from run import app


@pytest.fixture
def auth():
    return firebase_config.AUTH


@pytest.fixture
def client(request):
    os.environ['SMARTLOCK_MODE'] = "TEST"
    app.config['TESTING'] = True
    client = app.test_client()

    def fin():
        firebase_config.DB.remove()
    request.addfinalizer(fin)

    return client


@pytest.fixture
def db():
    return firebase_config.DB


@pytest.fixture
def firebase_test_config():
    config = ConfigParser()
    config.read('env/variables.ini')
    return config['FIREBASE_TEST_CONFIG']


@pytest.fixture
def id_token(firebase_test_config):

    test_email = firebase_test_config['testUsername']
    test_password = firebase_test_config['testPassword']
    user = firebase_config.AUTH.sign_in_with_email_and_password(
        test_email, test_password)
    return user['idToken']


@pytest.fixture
def mock_lock():
    return Lock()


@pytest.fixture
def default_password():
    return "123456"


@pytest.fixture
def get_mock_password(default_password):
    def actual_fixture(password=default_password, hashed=False):
        if hashed:
            plaintext = bytes(password, 'utf-8')
            return str(bcrypt.hashpw(plaintext, bcrypt.gensalt()), 'utf8')
        else:
            return password
    return actual_fixture


@pytest.fixture
def mock_password(get_mock_password, default_password) -> Password:
    return Password(
        type=PasswordType.UNLIMITED,
        password=get_mock_password(default_password, hashed=True),
    )


@pytest.fixture
def mock_user(auth, id_token, firebase_test_config):
    user_id = auth.get_account_info(id_token)['users'][0]['localId']
    return User(
        id=user_id,
        email=firebase_test_config['testUsername'],
        name=firebase_test_config['testName'],
    )


@pytest.fixture
def seeded_lock(db, mock_lock):
    id = db.child("Locks").push(mock_lock.serialize())['name']
    mock_lock.id = id
    return mock_lock


@pytest.fixture
def seed_password(db):
    def actual(password: Password, lock: Lock):
        new_id = db.child("Locks").child(lock.id).child("passwords").push(
            password.serialize())['name']
        password.id = new_id
        return password
    return actual


@pytest.fixture
def seeded_password(db, mock_password, seeded_lock, seed_password):
    return seed_password(password=mock_password, lock=seeded_lock)


@pytest.fixture
def seeded_user_lock(seeded_user, seeded_lock, db):
    db.child("UserLocks").child(seeded_user.id).set(
        {
            "ownedLockIds": [seeded_lock.id]
        }
    )
    return UserLocks(
        owned_lock_ids=[seeded_lock.id]
    )


@pytest.fixture
def seeded_user(db, auth, id_token, mock_user):
    user_id = mock_user.id
    db.child("Users").child(user_id).set(
        mock_user.serialize()
    )
    return mock_user


@pytest.fixture
def seeded_admin_user(db, seeded_user):
    db.child("Users").child(seeded_user.id).update(
        {'isAdmin': True}
    )
    return seeded_user
