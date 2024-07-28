# server/__init__.py
import os
from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

cors = CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    with app.app_context():
        app_settings = os.getenv(
            "APP_SETTINGS", "project.server.config.DevelopmentConfig"
        )

        app.config.from_object(app_settings)

        cors.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)

        from project.server.api import api_blog
        api_blog.init_app(app)

    return app
