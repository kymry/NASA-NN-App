from flask import Flask, g
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from .config import Config
from . import front_end
from . import external_apis as ep
from . import sql_models

# Globally accessible objects
mongodb = PyMongo()
sqldb = SQLAlchemy()
migrate = Migrate()


def create_app():
    ''' Application factory method that creates and configures the Flask app object '''

    # create and configure the app. __name__ is set to the name of the module in which it is used
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():

        # Initialize MongoDB and SQLite3 connections
        mongodb.init_app(app)
        sqldb.init_app(app)
        migrate.init_app(app, sqldb)
        from .sql_models import Flare

        # register the front_end blueprint with the app (so that it can be accessed later)
        register_blueprints(app)

        # ML models
        #model = pickle.load(open('TODO.pickle', 'rb'))

        # these variables can be used in the '$ flask shell' context
        register_shell_context_variables(app)

        # start the job scheduler
        start_job_scheduler(app)

        return app


def register_blueprints(app):
    with app.app_context():
        app.register_blueprint(front_end.bp)


def register_shell_context_variables(app):
    @app.shell_context_processor
    def make_shell_context():
        return {'sqldb': sqldb, 'mongodb': mongodb, 'Flare': sql_models.Flare}


def start_job_scheduler(app):
    with app.app_context():
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        app.apscheduler.add_job(func=query_nasa_apis, args=[app], trigger='interval', days=1, id='call_apis')


def query_nasa_apis(app):
    with app.app_context():
        print('hello')
        ep.get_mars_weather_data(mongodb, sqldb)
        ep.get_solarflare_data(sqldb)

