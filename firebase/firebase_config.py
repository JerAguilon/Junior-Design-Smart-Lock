import pyrebase

from configparser import ConfigParser

config = ConfigParser()
config.read('env/variables.ini')
firebase_variables = config['FIREBASE_DEV_CONFIG']


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
