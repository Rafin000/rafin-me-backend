# project/server/config.py

import os


POSTGRES_SERVER_NAME = os.environ.get('POSTGRES_SERVER_NAME', 'localhost')
POSTGRES_USER_NAME = os.environ.get('POSTGRES_USER_NAME', 'postgres')
postgres_local_base = 'postgresql://' + POSTGRES_USER_NAME + ':postgres@' + POSTGRES_SERVER_NAME + ':5432/'
database_name = 'blogdb'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', '63eaQmNBpg')
    API_KEY = os.environ.get("API_KEY", "@Beginning@After@the@ENd@")
    DEBUG = False
    MAIL_USERNAME="marufulislam00000@gmail.com"
    MAIL_PASSWORD="jwuywnewjqnlxvbu"
    MAIL_PORT=465
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    MAIL_SERVER="smtp.gmail.com"
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    # SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    API_KEY = os.environ.get("API_KEY", "jdjsdjkscsjdj")
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'