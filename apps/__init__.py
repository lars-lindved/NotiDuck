import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    for module_name in ('home', 'authentication', 'dashboard', 'email'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(config_class):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    print(f"Instance path: {app.instance_path}")

    # Set up the database URI if not set in config
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'my_database.db')
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_extensions(app)
    register_blueprints(app)

    with app.app_context():
        # Import models to register them with SQLAlchemy
        from apps import models  # Ensure models are imported
        db.create_all()

    return app

