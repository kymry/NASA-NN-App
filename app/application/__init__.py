from flask import Flask
from flask_apscheduler import APScheduler
from logging.handlers import RotatingFileHandler
from config import Config
from external_apis import external_apis as ep
from routes import frontend
import os
import logging
import datetime


def create_app():
    ''' Application factory method that creates and configures the Flask app object '''

    app = Flask(__name__)
    app.config.from_object(Config)

    from models.models import db, mongodb, migrate, login

    # Initialize plugins with the app object
    mongodb.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # within this block, current_app points to app
    with app.app_context():
        register_blueprints(app)
        register_shell_context_variables(app, db, mongodb)
        start_job_scheduler(app, db, mongodb)
        configure_logging(app)

        return app


def register_blueprints(app):
    with app.app_context():
        app.register_blueprint(frontend.bp)


def register_shell_context_variables(app, db, mongodb):
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'mongodb': mongodb}


def start_job_scheduler(app, db, mongodb):
    with app.app_context():
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        app.apscheduler.add_job(func=ep.query_apis, args=[app, mongodb, db],
                                trigger='interval', minutes=5, id='call_apis')


def configure_logging(app):
    with app.app_context():
        if not os.path.exists(os.getcwd() + '/logs'):
            os.mkdir(os.getcwd() + '/logs')
        file_handler = RotatingFileHandler('logs/application_error_log.log', maxBytes=10240)
        file_handler.setFormatter(logging.Formatter( '%(asctime)s %(levelname)s: %(message)s in %(pathname)s:%(lineno)d'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.DEBUG)