from flask import Flask, g
from flask_pymongo import PyMongo
import api.external_apis as nasa_api
from .config import Config

# Globally accessible libraries
mongo = PyMongo()


def create_app():
    ''' Application factory method --- creates and configures the Flask app object '''

    # create and configure the app. __name__ is set to the name of the module in which it is used
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLite3 and MongoDB
    from . import db
    db.init_app(app)
    mongo.init_app(app)

    # register the front_end blueprint with the app (so that it can be accessed later)
    with app.app_context():
        from . import front_end
        app.register_blueprint(front_end.bp)

        # ML models
        #model = pickle.load(open('TODO.pickle', 'rb'))

        # update mars data
        nasa_api.get_mars_data(mongo)

        return app
