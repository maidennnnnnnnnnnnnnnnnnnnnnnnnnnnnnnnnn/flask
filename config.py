from os import environ


class Config(object):
    FLASK_DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = "asdasd"
    FLASK_SECRET = SECRET_KEY

    # Login manager
    LOGIN_MANAGER_LOGIN_VIEW = "login"
    LOGIN_MANAGER_LOGIN_MESSAGE_CATEGORY = "info"

    # Images
    UPLOAD_FOLDER = 'app/static/images'
    ALLOWED_EXTENSIONS = {'jpg', 'png'}

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///feedbacks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_config():
        return config[environ.get('CONFIG') or "DEFAULT"]


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProdConfig(Config):
    DEVELOPMENT = False
    DEBUG = False

config = {
    'DEV': DevConfig,
    'PROD': ProdConfig,
    'DEFAULT': DevConfig,
}


#

#
