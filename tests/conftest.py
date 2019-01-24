import os
import pytest
from importlib import reload

from firebase import firebase_config


@pytest.fixture
def client(scope="session", autouse=True):
    print("YAY")
    os.environ['SMARTLOCK_MODE'] = "TEST"
    reload(firebase_config)
    return None
