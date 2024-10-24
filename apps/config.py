# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, random, string

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
    
    # Set up the App SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join('instance', 'my_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Mail configurations
    MAIL_SERVER = 'email-smtp.eu-west-1.amazonaws.com'  # Replace with your AWS SMTP server region
    MAIL_PORT = 587  # or 465 for SSL
    MAIL_USE_TLS = True  # Use TLS
    MAIL_USE_SSL = False  # Use SSL if MAIL_PORT is 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Your AWS WorkMail SMTP username
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Your AWS WorkMail SMTP password
    MAIL_DEFAULT_SENDER = ('Noti Duck', 'info@notiduck.com')
    
    
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
