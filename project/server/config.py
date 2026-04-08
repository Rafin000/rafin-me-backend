# project/server/config.py

import os
from datetime import timedelta


POSTGRES_SERVER_NAME = os.environ.get('POSTGRES_SERVER_NAME', 'localhost')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'blogdb')

postgres_base = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_NAME}:5432/'
database_name = POSTGRES_DB


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    # Base URL prepended to asset keys stored in the DB
    # (e.g. "https://nexora-uploads.s3.us-east-1.amazonaws.com/")
    S3_BASE_URL = os.environ.get('S3_BASE_URL', '')
    # AWS credentials + bucket config for the upload endpoint.
    # If any of these are missing, /api/v1/uploads returns 503.
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    S3_BUCKET = os.environ.get('S3_BUCKET', '')
    S3_UPLOAD_PREFIX = os.environ.get('S3_UPLOAD_PREFIX', 'rafin-assets')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB upload cap
    DEBUG = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.sendgrid.net')
    # "From" address that visible on outgoing emails. MUST be a sender
    # verified in your SendGrid account (or whichever provider).
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    # Where contact form messages are delivered.
    MAIL_RECIPIENT = os.environ.get('MAIL_RECIPIENT')
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = postgres_base + database_name

    def __init__(self):
        for name in ('SECRET_KEY', 'JWT_SECRET_KEY', 'POSTGRES_PASSWORD'):
            if not os.environ.get(name):
                raise RuntimeError(f"Required environment variable {name} is not set")
