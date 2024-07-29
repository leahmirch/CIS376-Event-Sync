import os

class Config:
    # Secret key for securing sessions and cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///eventsync.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # General Flask app configurations
    DEBUG = True  # Turn off in production

    # Additional configurations can be added here
    # For example, configuration for email server
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
