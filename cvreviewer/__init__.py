from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from cvreviewer.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Log in or Sign up first.'
login_manager.login_message_category = "error"


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from cvreviewer.users.routes import users
    from cvreviewer.posts.routes import posts
    from cvreviewer.home.routes import home

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(home)

    return app
