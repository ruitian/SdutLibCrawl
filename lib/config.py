import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    import sys
    reload(sys)  # noqa
    sys.setdefaultencoding('utf-8')

    SECRET_KEY = (
        os.environ.get('SECRET_KEY') or
        u'\x97\xfa%\xab\xd2\xc2\xf8\xfc\xef\xaeTKDk\xc0\xe1//($\xc7\xc0'
    )

    CSRF_ENABLED = True

    SERVER_NAME = os.getenv('lib_SERVER_NAME')

    # pagination
    PROBLEM_PER_PAGE = 20
    CONTEST_PER_PAGE = 20
    STATUS_PER_PAGE = 50
    FOLLOWERS_PER_PAGE = 20
    FOLLOWING_PER_PAGE = 20
    UPLOAD_FOLDER = BASE_DIR + '/app/uploads'
    GRAVATAR_BASE_URL = 'http://gravatar.duoshuo.com/avatar/'

    # mongodb
    MONGODB_SETTINGS = {
        'db': 'sdutlib',
        'username': '',
        'password': '',
        'host': '127.0.0.1',
        'port': 27017
    }

    # redis
    REDIS_URL = 'redis://%s:%s/%s' % (
        os.environ.get('REDIS_HOST', 'localhost'),
        os.environ.get('REDIS_PORT', '6379'),
        os.environ.get('REDIS_DATABASE', '1'),
    )

    # celery
    CELERY_BROKER_URL = 'redis://%s:%s' % (
        os.environ.get('REDIS_HOST', 'localhost'),
        os.environ.get('REDIS_PORT', '6379')
    )
    CELERY_BROKER_BACKEND = 'redis://%s:%s' % (
        os.environ.get('REDIS_HOST', 'localhost'),
        os.environ.get('REDIS_PORT', '6379')
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
