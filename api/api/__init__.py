from flask import Flask, g
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
        from .sql_models import Sol  # must be placed after the db is initialized (terrible design I know)

        # register the front_end blueprint with the app (so that it can be accessed later)
        app.register_blueprint(front_end.bp)

        # ML models
        #model = pickle.load(open('TODO.pickle', 'rb'))

        # these variables can be used in the '$ flask shell' context
        register_shell_context_variables(app)

        # update mars data
        ep.get_mars_weather_data(mongodb, sqldb)

        return app


def register_shell_context_variables(app):
    @app.shell_context_processor
    def make_shell_context():
        return {'sqldb': sqldb, 'mongodb': mongodb, 'Sol': sql_models.Sol}

