import pyrebase
import logging
import os

from configparser import ConfigParser

logger = logging.getLogger('firebase_config')

env_mode = os.environ.get('SMARTLOCK_MODE', "TEST")
if env_mode == "DEV":
    config = ConfigParser()
    config.read('env/variables.ini')
    firebase_variables = config['FIREBASE_DEV_CONFIG']
elif env_mode == "TEST":
    config = ConfigParser()
    config.read('env/variables.ini')
    firebase_variables = config['FIREBASE_TEST_CONFIG']
else:
    raise ValueError(
        "SMARTLOCK_MODE environment variable not found or invalid: {}".format(
            env_mode)
    )

logger.info('%s environment mode set', env_mode)


config = {
    "apiKey": firebase_variables['apiKey'],
    "authDomain": firebase_variables['authDomain'],
    "databaseURL": firebase_variables['databaseURL'],
    "storageBucket": firebase_variables['storageBucket'],
    "serviceAccount": firebase_variables['serviceAccount'],
}

FIREBASE_APP = pyrebase.initialize_app(config)
AUTH = FIREBASE_APP.auth()
DB = FIREBASE_APP.database()
