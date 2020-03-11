import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.urandom(24)
    
class Production(Config):
    DEVELOPMENT = False
    DEBUG = False
    
class Staging(Config):
    DEVELOPMENT = True
    DEBUG = True

class Testing(Config):
    DEVELOPMENT = True
    DEBUG = True