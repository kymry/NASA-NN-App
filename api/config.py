''' Set the configuration variables for Flask here '''
import os

DEBUG = True  # Turns on debugging features in Flask
MONGO_URI = os.environ.get('DB')