from os import environ
host = 'localhost'
port = 5000

debug = True
if environ.get('LASALCA_PROD'):
    debug = False

SQLALCHEMY_DATABASE_URI = 'postgres://***REMOVED***'
if environ.get('LASALCA_SASALCA'):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

APPLICATION_MOUNT = '/api'
SECRET_KEY = '***REMOVED***'
