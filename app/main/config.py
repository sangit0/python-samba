import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

SOCIAL_GOOGLE = {
    'consumer_key': 'xxxx',
    'consumer_secret': 'xxxx'
}


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SOCIAL_KEY = SOCIAL_GOOGLE
    CORS_HEADERS = 'Content-Type'
    LOG_TYPE = 'timed_rotating_file'
    LOG_LEVEL = 'DEBUG'
    LOG_DIR = './logs/'
    APP_LOG_NAME = './app.log'
    WWW_LOG_NAME = './access.log'    
    SAMBA_IP = 'localhost'
    SAMBA_BACKEND_PYTHON = 'localhost:5000/api/samba'
    SAMBA_USER="murad"
    SAMBA_USER_PASS="Selise1234"


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    LOG_TYPE = 'stream'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class StagingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    staging=StagingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
