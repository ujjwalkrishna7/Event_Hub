from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from event.config import Config # type: ignore



db = SQLAlchemy()
admin = Admin()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)    

    db.init_app(app)
    admin.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    from event.users.routes import users # type: ignore
    from event.events.routes import events # type: ignore
    from event.main.routes import main # type: ignore
    from event.errors.handlers import errors # type: ignore
    app.register_blueprint(users)
    app.register_blueprint(events)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app


