from flask import Flask, g
from flask_pymongo import PyMongo
import api.external_apis as nasa_api
from .config import Config
from . import front_end
from . import db

# Globally accessible
mongo = PyMongo()


def create_app():
    ''' Application factory method --- creates and configures the Flask app object '''

    # create and configure the app. __name__ is set to the name of the module in which it is used
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():

        # Initialize SQLite3 and MongoDB
        mongo.init_app(app)
        db.init_app(app)

        # register the front_end blueprint with the app (so that it can be accessed later)
        app.register_blueprint(front_end.bp)

        # ML models
        #model = pickle.load(open('TODO.pickle', 'rb'))

        # these variables can be used in the '$ flask shell'
        @app.shell_context_processor
        def make_shell_context():
            return {'db': db, 'mongo': mongo}

        # update mars data
        nasa_api.get_mars_data(mongo)

        return app
