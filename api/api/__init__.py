from flask import Flask, g
from flask_pymongo import PyMongo

# Globally accessible libraries
mongo = PyMongo()


def create_app():
    ''' Application factory method --- creates and configures the Flask app object '''

    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG=True,  # Turns on debugging features in Flask
        MONGO_URI="mongodb://127.0.0.1:27017/marsdata"  # Connects to MongoDB running on localhost on port 27017
    )

    # Initialize plugins
    mongo.init_app(app)

    # register the front_end blueprint with the app (so that it can be accessed later)
    with app.app_context():
        from . import front_end
        app.register_blueprint(front_end.bp)

        # ML models
        #model = pickle.load(open('TODO.pickle', 'rb'))

        return app
