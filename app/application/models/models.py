from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, LoginManager

# globally accessible variables - instantiated in this module to avoid circular imports
login = LoginManager()
login.login_view = 'login'
mongodb = PyMongo()
db = SQLAlchemy()
migrate = Migrate()


# decorator registers the method with Flask-Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# db.Model is a base class for all models from Flask-SQLAlchemy
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

    def __repr__(self):
        return 'Username: {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_subscribed(self, api_id):
        sub = Subscription.query.filter_by(user_id=current_user.id, subscription_id=api_id).first()
        return True if sub else False

    def subscribe(self, api_id):
        sub = Subscription(user_id=current_user.id, subscription_id=api_id)
        db.session.add(sub)
        db.session.commit()

    def unsubscribe(self, api_id):
        sub = Subscription.query.filter_by(user_id=current_user.id, subscription_id=api_id).first()
        db.session.delete(sub)
        db.session.commit()

    def get_subscriptions(self):
        raw_subs = Subscription.query.filter_by(user_id=current_user.id).all()
        return [SubscriptionDetails.query.filter_by(id=x.subscription_id).first().name for x in raw_subs]


class Subscription(db.Model):
    """
    Subscription ids:
        1: Apod
        2: Sol
        3: Flare
    """
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    subscription_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'user {} is subscribed to api {}'.format(self.user_id, self.subscription_id)


class SubscriptionDetails(db.Model):
    id = db.Column(db.Integer, db.ForeignKey(Subscription.subscription_id), primary_key=True)
    name = db.Column(db.String)

    @classmethod
    def get_all_subscriptions(cls):
        live_subscriptions = db.session.query(SubscriptionDetails).all()
        return [{'id': str(sub.id), 'name': sub.name} for sub in live_subscriptions]

    def __repr__(self):
        return 'Subscription id {} is named {}'.format(self.id, self.name)


class Apod(db.Model):
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

