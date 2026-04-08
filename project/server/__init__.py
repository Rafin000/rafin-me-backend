# server/__init__.py
import os
from flask import Flask, request
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter


def client_ip():
    """
    Return the best-effort real client IP, favouring Cloudflare's header
    over the raw X-Forwarded-For chain.
    """
    return (
        request.headers.get('CF-Connecting-IP')
        or request.headers.get('X-Real-IP')
        or (request.headers.get('X-Forwarded-For') or '').split(',')[0].strip()
        or request.remote_addr
        or 'unknown'
    )


cors = CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()
# In-memory storage is fine for a single-VM deployment. Each gunicorn
# worker keeps its own counters, which means an attacker could in theory
# get (limit * num_workers) requests through due to load balancing.
# For a contact form with a 3/hour cap, that's acceptable.
limiter = Limiter(
    key_func=client_ip,
    storage_uri='memory://',
    headers_enabled=True,
)


def create_app():
    app = Flask(__name__)

    with app.app_context():
        app_settings = os.getenv(
            "APP_SETTINGS", "project.server.config.DevelopmentConfig"
        )

        app.config.from_object(app_settings)
        cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)
        mail.init_app(app)
        jwt.init_app(app)
        limiter.init_app(app)

        from project.server.api import api_blog
        api_blog.init_app(app)

    return app
