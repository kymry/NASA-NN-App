import os
# __file__ is the pathname of the file from which the module was loaded
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ All configurations for the app """
    DEBUG = True  # Turns on debugging features in Flask
    MONGO_URI = "mongodb://127.0.0.1:27017/marsdata"  # Connects to MongoDB running on localhost on port 27017
    SECRET_KEY = os.environ.get('SECRET_KEY') or "H49J*dE#4kslf"  # needed for Flask-WTF form security
    DATABASE = os.environ.get('DATABASE') or os.path.join(basedir, 'databases/astronomicaldata.db')
    # 'sqlite:///' tells SQLAlchemy which database engine to use
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'databases/astronomicaldata.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # if True, signals a change every time an update is made to the db


if __name__ == "__main__":
    print(basedir)
