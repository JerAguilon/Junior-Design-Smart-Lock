import os


def test_basic():
    assert os.environ['SMARTLOCK_MODE'] == 'TEST'
