import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a_default_jwt_secret_key'
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql://user:password@localhost/test_dbname'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}

key = Config.SECRET_KEY