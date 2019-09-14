host = 'localhost'
port = 5000

from os import environ
debug = True
if environ.get('LASALCA_PROD'):
    debug = False

SQLALCHEMY_DATABASE_URI = 'postgres://***REMOVED***'
if environ.get('LASALCA_SASALCA'):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
