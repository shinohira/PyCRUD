class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = ''

class DevConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = ''
    HOST = ''
    DATABASE = ''
    USER = ''
    PASSWORD = ''

class HerokuConfig(object):
    DEBUG = False
    SECRET_KEY = ''
    HOST = ''
    DATABASE = ''
    USER = ''
    PASSWORD = ''
