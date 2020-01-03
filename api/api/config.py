import os


class Config():
    """ All configurations for the app """
    DEBUG = True  # Turns on debugging features in Flask
    MONGO_URI = "mongodb://127.0.0.1:27017/marsdata"  # Connects to MongoDB running on localhost on port 27017
    SECRET_KEY = os.environ.get('SECRET_KEY') or "H49J*dE#4kslf" # needed for Flask-WTF form security
    DATABASE = "'/Users/kymryburwell/Google Drive/Code Repository/NASA ML API/api/databases/marsweather.sqlite3'"
