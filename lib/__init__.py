# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from .config import config


app = Flask(__name__)
db = MongoEngine()
login_manager = LoginManager()


with app.app_context():
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .views import(
        bp_auth,
        bp_index
    )

    app.register_blueprint(
        bp_auth,
        url_prefix='/auth'
    )
    app.register_blueprint(
        bp_index,
        url_prefix='/'
    )
