from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from .config import Config
from .external_apis import external_apis as ep
from .services import front_end


mongodb = PyMongo()
sqldb = SQLAlchemy()
migrate = Migrate()


def create_app():
    ''' Application factory method that creates and configures the Flask app object '''

    # create and configure the app. __name__ is set to the name of the module in which it is used
    app = Flask(__name__)
    app.config.from_object(Config)

    # within this block, current_app points to app
    with app.app_context():

        # Initialize MongoDB and SQLite3 connections
        mongodb.init_app(app)
        sqldb.init_app(app)
        migrate.init_app(app, sqldb)

        # register the front_end blueprint with the app (so that it can be accessed later)
        register_blueprints(app)

        # these variables can be used in the '$ flask shell' context
        register_shell_context_variables(app)

        #start_job_scheduler(app, mongodb, sqldb)
        ep.query_apod_api(sqldb)

        return app


def register_blueprints(app):
    with app.app_context():
        app.register_blueprint(front_end.bp)


def register_shell_context_variables(app):
    @app.shell_context_processor
    def make_shell_context():
        return {'db': sqldb, 'mongodb': mongodb}


def start_job_scheduler(app, mongodb, sqldb):
    with app.app_context():
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        app.apscheduler.add_job(func=ep.query_apis, args=[app, mongodb, sqldb],
                                trigger='interval', days=1, id='call_apis')

