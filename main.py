import os
from flask import Flask, render_template
from flask_login import LoginManager
from application import *
from application.config import LocalDevelopmentConfig
from application.database import db
from application.controller import app as main
from flask_bcrypt import Bcrypt
from application.models import User 

app = None



def create_app():
    app = Flask(__name__, template_folder = "templates")
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "controller.login"
    login_manager.user_loader(load_user)
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production to config")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(main)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    