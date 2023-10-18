from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from application.models import User
from .config import Config, LocalDevelopmentConfig

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

def load_user(user_id):
    return User.query.get(int(user_id))