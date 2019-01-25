import os
import pytest

from configparser import ConfigParser
from importlib import reload

from firebase import firebase_config
from run import app


@pytest.fixture
def client(request):
    os.environ['SMARTLOCK_MODE'] = "TEST"
    app.config['TESTING'] = True
    client = app.test_client()

    def fin():
        print("FINALIZING STUFF")
        firebase_config.DB.remove()
    request.addfinalizer(fin)

    return client


@pytest.fixture
def id_token():
    config = ConfigParser()
    config.read('env/variables.ini')
    test_config = config['FIREBASE_TEST_CONFIG']

    test_email = test_config['testUsername']
    test_password = test_config['testPassword']
    user = firebase_config.AUTH.sign_in_with_email_and_password(
        test_email, test_password)
    return user['idToken']
