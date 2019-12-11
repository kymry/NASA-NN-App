from flask_pymongo import PyMongo  # uses MongoDb's Python client API internally
from flask import current_app, g  # current_app points to the Flask app handling the request


def get_db():

    # g is a special flask object that will store data it thinks will be used for multiple requests
        # configure the database (Flask object is sent as parameter to PyMango
    g.db = PyMongo(current_app)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    #  TODO - may need to change this to work with MongoDB
    if db is not None:
        db.close()


def init_app(app):
    ''' Registers all functions with the app instance '''
    app.cli.add_command(get_db)

