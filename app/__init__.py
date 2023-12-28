from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mm = Marshmallow()
basic_auth = HTTPBasicAuth(scheme='Bearer')

def create_app(config_class=Config.get_config()):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)

    db.init_app(app)
    mm.init_app(app)
    JWTManager(app)
    login_manager.init_app(app)
    login_manager.login_view = config_class.LOGIN_MANAGER_LOGIN_VIEW
    login_manager.login_message_category = config_class.LOGIN_MANAGER_LOGIN_MESSAGE_CATEGORY

    with app.app_context():

        from .api import api_bp
        from app.teacher_api import teacher_bp

        from app.auth import auth_bp
        from app.main import main_bp
        from app.todo import todo_bp
        from app.user import user_bp

        app.register_blueprint(api_bp, url_prefix="/api")
        app.register_blueprint(teacher_bp, url_prefix="/api")
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(main_bp, url_prefix="/main")
        app.register_blueprint(todo_bp, url_prefix="/todo")
        app.register_blueprint(user_bp, url_prefix="/user")

        from . import views

    return app


config = Config.get_config()

app = create_app(config)

Migrate(app, db)



# from flask import Flask
# from flask_httpauth import HTTPBasicAuth
# from flask_jwt_extended import JWTManager
# from flask_login import LoginManager
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
#
# from config import *
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# db = SQLAlchemy(app)
# app.config['SECRET_KEY'] = SECRET_KEY
# asd = Migrate(app, db)
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
#
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
#
#
# from .api import api_bp
#
# app.register_blueprint(api_bp, url_prefix='/api')
#
# from app import views
