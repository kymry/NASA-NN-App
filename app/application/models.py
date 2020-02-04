from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

mongodb = PyMongo()
db = SQLAlchemy()
migrate = Migrate()


# db.Model is a base class for all models from Flask-SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return 'User {}'.format(self.username)


class Apod(db.Model):
    """ Astronomy Picture of the Day (APOD) """
    date = db.Column(db.String, primary_key=True)
    explanation = db.Column(db.String)
    media_type = db.Column(db.String)
    title = db.Column(db.String)
    url = db.Column(db.String)
    path = db.Column(db.String)

    def __repr__(self):
        return 'Astronomy Picture of the Day: {}'.format(self.title)


class Sol(db.Model):
    sol = db.Column(db.Integer, primary_key=True)
    average_temperature = db.Column(db.Float)
    high_temperature = db.Column(db.Float)
    low_temperature = db.Column(db.Float)
    horizontal_wind_speed = db.Column(db.Float)
    pressure = db.Column(db.Float)

    def __repr__(self):
        return 'sol: {}'.format(self.sol)


class Flare(db.Model):
    id = db.Column(db.String, primary_key=True)
    begin_time = db.Column(db.DateTime)
    peak_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    class_type = db.Column(db.String)
    activity_region = db.Column(db.String)

    def __repr__(self):
        return 'flare: {}'.format(self.id)
